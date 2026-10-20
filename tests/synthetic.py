"""Template-generated documents with known conditions, for testing learners end to end.

These are synthetic test fixtures, not gold annotations of real advisories.
"""

from __future__ import annotations

import random

from tests.factories import make_doc
from triggermap.ingest.records import AdvisoryDocument
from triggermap.schema.models import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.preprocessing import PreprocessedDocument, compose_raw, preprocess

U, C, A = Category.USAGE, Category.CONFIGURATION, Category.ACCESS
REQ, EXC = Role.REQUIRED, Role.EXCEPTION

TRAIN_VOCAB = {
    "lib": ["aiohttp", "flask", "django", "tornado", "starlette", "bottle"],
    "mode": ["web server", "reverse proxy", "worker", "client"],
    "feature": ["static routes", "file uploads", "template caching", "debug pages"],
    "flag": ["follow_symlinks", "allow_pickle", "trust_remote_code", "debug_mode"],
    "actor": ["user", "administrator", "editor", "operator"],
    "thing": ["CLI", "HTTP API", "admin panel", "scheduler"],
}
TEST_VOCAB = {
    "lib": ["sanic", "falcon"],
    "mode": ["gateway", "daemon"],
    "feature": ["websocket streaming", "session storage"],
    "flag": ["unsafe_eval", "skip_verify"],
    "actor": ["maintainer", "reviewer"],
    "thing": ["RPC endpoint", "plugin loader"],
}

Spec = tuple[str, Category, Role]

_GHSA_ALPHABET = "23456789cfghjmpqrvwx"
_STREAMS = {"train": 0, "test": 1, "x": 2, "t": 3, "pos": 4, "cli": 5}


def synthetic_id(prefix: str, index: int) -> str:
    """A well-formed GHSA id that encodes the dataset stream and the index."""
    digits = []
    for _ in range(8):
        index, rem = divmod(index, 20)
        digits.append(_GHSA_ALPHABET[rem])
    tail = "".join(reversed(digits))
    return f"GHSA-{_GHSA_ALPHABET[_STREAMS[prefix]] * 4}-{tail[:4]}-{tail[4:]}"


def _templates(v: dict[str, str]) -> list[tuple[str, list[Spec], GroupOperator | None]]:
    return [
        (
            f"When using {v['lib']} as a {v['mode']} and enabling {v['feature']}, "
            "attackers can read files.",
            [(f"using {v['lib']} as a {v['mode']}", U, REQ), (f"enabling {v['feature']}", U, REQ)],
            GroupOperator.ALL,
        ),
        (
            f"Only affects deployments with {v['flag']} set to True.",
            [(f"{v['flag']} set to True", C, REQ)],
            None,
        ),
        (f"A crash occurs in the {v['feature']} parser.", [], None),
        (
            f"The issue is exploitable unless {v['flag']} is disabled.",
            [(f"{v['flag']} is disabled", C, EXC)],
            None,
        ),
        (
            f"An authenticated {v['actor']} can trigger the bug.",
            [(f"authenticated {v['actor']}", A, REQ)],
            None,
        ),
        (
            f"Exposure happens when using the {v['thing']} or using the {v['feature']} module.",
            [(f"using the {v['thing']}", U, REQ), (f"using the {v['feature']} module", U, REQ)],
            GroupOperator.ANY,
        ),
    ]


def make_dataset(
    n: int, vocab: dict[str, list[str]], seed: int, prefix: str
) -> list[tuple[AdvisoryDocument, PreprocessedDocument, AdvisoryAnnotation]]:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        v = {k: rng.choice(words) for k, words in vocab.items()}
        text, specs, operator = rng.choice(_templates(v))
        aid = synthetic_id(prefix, i)
        doc = make_doc(aid, text, (v["lib"],), summary="Synthetic advisory")
        pre = preprocess(compose_raw(doc.summary, doc.details))
        conditions = []
        for k, (surface, category, role) in enumerate(specs):
            start = pre.text.index(surface)
            conditions.append(
                Condition(
                    id=f"c{k + 1}", span=(start, start + len(surface)), category=category, role=role
                )
            )
        groups = (
            (Group(operator=operator, members=tuple(c.id for c in conditions)),) if operator else ()
        )
        record = AdvisoryAnnotation(
            advisory_id=aid,
            source_commit="c" * 40,
            content_hash=pre.content_hash,
            preprocessing_version=pre.version,
            annotation_version="synthetic",
            document_status=(
                DocumentStatus.HAS_CONDITIONS
                if conditions
                else DocumentStatus.NO_EXPLICIT_CONDITION
            ),
            conditions=tuple(conditions),
            groups=groups,
        )
        out.append((doc, pre, record))
    return out
