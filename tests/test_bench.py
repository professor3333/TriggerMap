import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

import pytest

from tests.factories import make_doc
from triggermap.bench.environment import describe
from triggermap.bench.load import load_test
from triggermap.bench.report import TARGETS, render
from triggermap.bench.worker import BenchConfig, _summary, parse_config, run
from triggermap.bench.workload import BUCKETS, build_workload


class WordTokenizer:
    """Stand-in tokenizer: one token per whitespace-separated word."""

    def __call__(self, text: str, **_: Any) -> dict[str, list[int]]:
        return {"input_ids": list(range(len(text.split())))}


def test_parse_config_and_names() -> None:
    config = parse_config("kind=onnx,dir=/m,threads=2,batch=4")
    assert config == BenchConfig("onnx", "/m", 2, 4)
    assert config.name == "onnx-t2-b4"
    assert parse_config("kind=rules,label=baseline").name == "baseline"


def test_summary_percentiles() -> None:
    stats = _summary([float(i) for i in range(1, 101)])
    assert (stats["n"], stats["p50"], stats["p95"], stats["max"]) == (100, 51.0, 95.0, 100.0)


def test_workload_buckets_by_length_and_skips_test_pool() -> None:
    docs = [
        make_doc(f"GHSA-2222-2222-{i:04d}", "word " * n, ("p",))
        for i, n in enumerate([500, 520, 1800, 2000, 30, 40])
    ]
    docs.append(make_doc("GHSA-2222-2222-9999", "word " * 510, ("p",)))  # test pool
    split = {
        "assignment": {d.advisory_id: "train" for d in docs[:-1]} | {docs[-1].advisory_id: "test"}
    }
    workload = build_workload(docs, split, WordTokenizer(), per_bucket=5, natural=10)
    assert {i["advisory_id"] for i in workload["buckets"]["~512"]} == {
        docs[0].advisory_id,
        docs[1].advisory_id,
    }
    for name, (low, high) in BUCKETS.items():
        assert all(low <= i["tokens"] <= high for i in workload["buckets"][name])
    every = [i["advisory_id"] for items in workload["buckets"].values() for i in items]
    assert docs[-1].advisory_id not in every
    assert workload["natural_token_distribution"]["max"] >= 2000


def test_worker_runs_rules_in_process() -> None:
    docs = {
        "a": "Only affects deployments using the legacy API. " * 20,
        "b": "When debug_mode=True is set, files leak. " * 80,
    }
    workload = {
        "buckets": {
            "~512": [{"advisory_id": "a", "tokens": 500}],
            "~2000": [{"advisory_id": "b", "tokens": 2000}],
            "natural": [{"advisory_id": "a", "tokens": 500}, {"advisory_id": "b", "tokens": 2000}],
        }
    }
    result = run(BenchConfig("rules"), workload, docs, repeats=2)
    assert result["model_id"] == "rules-2"
    assert result["buckets"]["~512"]["n"] == 2 and result["buckets"]["natural"]["docs_per_s"] > 0
    assert result["peak_rss_mb"] > 0 and result["cold_start"]["total_s"] > 0


def fake_result(p95_512: float, rss: float) -> dict[str, Any]:
    return {
        "config": {"name": "x"},
        "model_id": "m",
        "cold_start": {"imports_s": 1, "load_s": 1, "first_extraction_s": 1, "total_s": 3},
        "buckets": {
            "~512": {"p50": 1.0, "p95": p95_512},
            "~2000": {"p50": 2.0, "p95": 5.0},
            "natural": {"docs_per_s": 1.0},
        },
        "peak_rss_mb": rss,
    }


def test_report_judges_targets_only_on_the_target_host() -> None:
    workload = {
        "version": "w",
        "source": "s",
        "tokenizer": {"name": "t"},
        "natural_token_distribution": {"p50": 1},
    }
    env = describe() | {"matches_target_host": False}
    proxy = render("t", env, workload, [fake_result(3.0, 100)])
    assert "Local proxy run" in proxy and "❌" not in proxy and "✅" not in proxy
    target = render("t", env | {"matches_target_host": True}, workload, [fake_result(3.0, 100)])
    assert "❌" in target and "✅" in target  # 3.0 s misses p95 <= 2.5; memory passes
    assert f"≤ {TARGETS['p95_512_s']}" in target


def test_environment_description() -> None:
    env = describe()
    assert {"machine", "cpu_model", "logical_cpus", "matches_target_host"} <= set(env)


class Handler(BaseHTTPRequestHandler):
    calls = 0

    def do_POST(self) -> None:
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        Handler.calls += 1
        status = 503 if "fail" in body["text"] else 200
        self.send_response(status)
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *args: Any) -> None:
        pass


@pytest.fixture
def server() -> Any:
    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def test_load_test_counts_successes_and_bypasses_cache(server: str) -> None:
    result = load_test(server, ["ok text", "fail text"], requests=20, concurrency=4)
    assert result["requests"] == 20 and result["succeeded"] == 10
    assert result["success_rate"] == 0.5 and result["status_counts"] == {"200": 10, "503": 10}
    assert result["cache"].startswith("bypassed") and result["latency_s"]["p95"] is not None


def test_committed_workload_is_well_formed() -> None:
    root = Path(__file__).resolve().parents[1]
    workload = json.loads((root / "reports/benchmarks/workload-v1.json").read_text())
    split = json.loads((root / "splits/pool-v1.json").read_text())
    for items in workload["buckets"].values():
        for item in items:
            assert split["assignment"][item["advisory_id"]] in ("train", "dev")
    assert len(workload["buckets"]["~512"]) == len(workload["buckets"]["~2000"]) == 20


def test_run_configs_checkpoints_and_resumes(tmp_path: Path) -> None:
    from triggermap.bench.report import run_configs

    processed = tmp_path / "processed"
    processed.mkdir()
    doc = make_doc("GHSA-2222-2222-2222", "Only affects deployments using the legacy API.")
    (processed / "advisories.jsonl").write_text(doc.model_dump_json() + "\n")
    item = {"advisory_id": doc.advisory_id, "tokens": 9}
    workload = tmp_path / "workload.json"
    workload.write_text(json.dumps({"buckets": {"~512": [item], "~2000": [], "natural": [item]}}))
    checkpoint = tmp_path / "run.partial.jsonl"
    first = run_configs([BenchConfig("rules", label="r")], workload, processed, 1, checkpoint)
    assert len(checkpoint.read_text().splitlines()) == 1
    # Same name, but this configuration would crash if it actually ran: it must be reused.
    again = run_configs(
        [BenchConfig("no-such-kind", label="r")], workload, processed, 1, checkpoint
    )
    assert again == first
