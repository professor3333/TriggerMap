"""Fine-tuning loop for the transformer extractor.

Pretrained tokenizer and encoder are reused; the new heads are trained and the encoder is
fine-tuned. Model selection uses typed-condition F1 on the dev split with early stopping.
Class weights come from training data only. Mixed precision is used on CUDA.

Every run records the base checkpoint revision, training and split hashes, hyperparameters,
seed, per-epoch dev metrics, training time and peak GPU memory, in the bundle metadata and,
when an experiment name is given, in MLflow.
"""

from __future__ import annotations

import copy
import random
import time
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import torch
from pydantic import BaseModel, ConfigDict
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup

from triggermap.eval.metrics import collect, summary
from triggermap.models.crf.model import training_hash
from triggermap.models.transformer.data import (
    BIO,
    CATEGORIES,
    GROUP_LABELS,
    ROLES,
    Window,
    WindowParams,
    make_windows,
)
from triggermap.models.transformer.extractor import TransformerExtractor, _collate, pick_device
from triggermap.models.transformer.model import (
    ConditionModel,
    LossWeights,
    batch_loss,
    inverse_frequency,
)
from triggermap.schema.models import AdvisoryAnnotation
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument

Example = tuple[PreprocessedDocument, AdvisoryAnnotation]


class TrainConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    model_id: str
    base_model: str  # hub id or local directory
    revision: str | None = None
    max_length: int = 512
    stride: int = 64
    context_tokens: int = 48
    use_context: bool = True  # ablation: heading/list context
    group_loss_weight: float = 1.0  # ablation: 0 removes the group objective
    attribute_loss_weight: float = 1.0
    learning_rate: float = 5e-5
    epochs: int = 4
    batch_size: int = 8
    gradient_accumulation: int = 2
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    patience: int = 2
    seed: int = 0
    device: str = "auto"
    max_train_documents: int | None = None  # learning curves
    mlflow_experiment: str | None = None
    split_assignment_sha256: str | None = None

    def window(self) -> WindowParams:
        return WindowParams(self.max_length, self.stride, self.context_tokens, self.use_context)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def class_weights(windows: Sequence[Window]) -> LossWeights:
    bio = Counter(t for w in windows for t in w.bio if t >= 0)
    category = Counter(s.category for w in windows for s in w.spans)
    role = Counter(s.role for w in windows for s in w.spans)
    group = Counter(p.label for w in windows for p in w.pairs)
    return LossWeights(
        inverse_frequency([bio[i] for i in range(len(BIO))]),
        inverse_frequency([category[i] for i in range(len(CATEGORIES))]),
        inverse_frequency([role[i] for i in range(len(ROLES))]),
        inverse_frequency([group[i] for i in range(len(GROUP_LABELS))]),
    )


def _batches(windows: Sequence[Window], size: int, rng: random.Random) -> list[list[Window]]:
    """Length-sorted buckets shuffled at batch level: little padding, still randomised."""
    ordered = sorted(windows, key=lambda w: (len(w.input_ids), rng.random()))
    batches = [list(ordered[i : i + size]) for i in range(0, len(ordered), size)]
    rng.shuffle(batches)
    return batches


def _dev_scores(extractor: TransformerExtractor, dev: Sequence[Example]) -> dict[str, float]:
    if not dev:
        return {}
    gold = {record.advisory_id: record for _, record in dev}
    preds = {record.advisory_id: extractor.extract(doc, record.advisory_id) for doc, record in dev}
    return summary(collect(gold, preds))  # type: ignore[arg-type]


def train(
    config: TrainConfig,
    train_examples: Sequence[Example],
    dev_examples: Sequence[Example],
    out_dir: Path,
) -> TransformerExtractor:
    set_seed(config.seed)
    rng = random.Random(config.seed)
    device = pick_device(config.device)
    examples = list(train_examples)
    if config.max_train_documents is not None:
        examples = rng.sample(examples, min(config.max_train_documents, len(examples)))

    tokenizer = AutoTokenizer.from_pretrained(config.base_model, revision=config.revision)
    # transformers 5 loads weights in their stored dtype (deberta-v3-small is stored in fp16).
    # Keep float32 master weights; mixed precision comes from autocast on CUDA.
    encoder = AutoModel.from_pretrained(
        config.base_model, revision=config.revision, dtype=torch.float32
    )
    base_revision = getattr(encoder.config, "_commit_hash", None) or config.revision
    model = ConditionModel(encoder).to(device)

    params = config.window()
    windows = [w for doc, record in examples for w in make_windows(doc, tokenizer, params, record)]
    if not windows:
        raise ValueError("no training windows")
    weights = class_weights(windows)
    weights.attribute_weight = config.attribute_loss_weight
    weights.group_weight = config.group_loss_weight
    weights = weights.to(device)

    steps_per_epoch = max(1, -(-len(windows) // config.batch_size) // config.gradient_accumulation)
    total_steps = steps_per_epoch * config.epochs
    no_decay = ("bias", "LayerNorm.weight", "layer_norm.weight")
    groups = [
        {
            "params": [p for n, p in model.named_parameters() if not n.endswith(no_decay)],
            "weight_decay": config.weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() if n.endswith(no_decay)],
            "weight_decay": 0.0,
        },
    ]
    optimizer = torch.optim.AdamW(groups, lr=config.learning_rate)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, int(config.warmup_ratio * total_steps), total_steps
    )
    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()

    metadata: dict[str, Any] = {
        "model_id": config.model_id,
        "family": "transformer",
        "base_model": config.base_model,
        "base_revision": base_revision,
        "preprocessing_version": PREPROCESSING_VERSION,
        "window": {
            "max_length": params.max_length,
            "stride": params.stride,
            "context_tokens": params.context_tokens,
            "use_context": params.use_context,
        },
        "config": config.model_dump(),
        "training_documents": len(examples),
        "training_hash": training_hash([record for _, record in examples]),
        "split_assignment_sha256": config.split_assignment_sha256,
        "windows": len(windows),
        "unreachable_spans": sum(w.unreachable for w in windows),
        "label_counts": {
            "category": dict(Counter(CATEGORIES[s.category] for w in windows for s in w.spans)),
            "role": dict(Counter(ROLES[s.role] for w in windows for s in w.spans)),
            "group_pairs": dict(Counter(GROUP_LABELS[p.label] for w in windows for p in w.pairs)),
        },
        "epochs": [],
    }
    tracker = _Tracker(config, metadata)
    extractor = TransformerExtractor(model, tokenizer, metadata, device, config.batch_size)
    pad_id = int(tokenizer.pad_token_id or 0)
    best_score, best_state, best_epoch, stale = -1.0, None, 0, 0
    started = time.monotonic()

    for epoch in range(1, config.epochs + 1):
        model.train()
        totals: Counter[str] = Counter()
        batches = _batches(windows, config.batch_size, rng)
        for step, chunk in enumerate(batches, start=1):
            batch = _collate(chunk, device, pad_id)
            with torch.autocast("cuda", dtype=torch.float16, enabled=use_amp):
                loss, parts = batch_loss(model, batch, weights)
            scaler.scale(loss / config.gradient_accumulation).backward()
            totals.update(parts)
            if step % config.gradient_accumulation == 0 or step == len(batches):
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                scheduler.step()
        model.eval()
        scores = _dev_scores(extractor, dev_examples)
        record = {
            "epoch": epoch,
            "train_loss": {k: round(v / len(batches), 5) for k, v in totals.items()},
            "dev": {k: round(v, 5) for k, v in scores.items()},
        }
        metadata["epochs"].append(record)
        tracker.epoch(epoch, record)
        score = scores.get("typed_f1", -float(sum(totals.values())))
        if score > best_score:
            best_score, best_epoch, stale = score, epoch, 0
            best_state = copy.deepcopy({k: v.detach().cpu() for k, v in model.state_dict().items()})
        else:
            stale += 1
            if stale >= config.patience:
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    metadata["best_epoch"] = best_epoch
    metadata["best_dev_typed_f1"] = best_score if dev_examples else None
    metadata["train_seconds"] = round(time.monotonic() - started, 1)
    metadata["peak_gpu_memory_mb"] = (
        round(torch.cuda.max_memory_allocated() / 2**20) if device.type == "cuda" else None
    )
    metadata["device"] = device.type
    extractor.save(out_dir)
    tracker.finish(metadata, out_dir)
    return extractor


class _Tracker:
    """MLflow logging when an experiment name is configured; a no-op otherwise."""

    def __init__(self, config: TrainConfig, metadata: dict[str, Any]) -> None:
        self.mlflow: Any = None
        if config.mlflow_experiment is None:
            return
        import mlflow

        self.mlflow = mlflow
        mlflow.set_experiment(config.mlflow_experiment)
        mlflow.start_run(run_name=config.model_id)
        mlflow.log_params(
            {
                **{k: v for k, v in config.model_dump().items() if v is not None},
                "base_revision": metadata["base_revision"],
                "training_hash": metadata["training_hash"],
                "training_documents": metadata["training_documents"],
                "preprocessing_version": metadata["preprocessing_version"],
            }
        )

    def epoch(self, epoch: int, record: dict[str, Any]) -> None:
        if self.mlflow is None:
            return
        metrics = {f"train_{k}": v for k, v in record["train_loss"].items()}
        metrics.update({f"dev_{k}": v for k, v in record["dev"].items()})
        self.mlflow.log_metrics(metrics, step=epoch)

    def finish(self, metadata: dict[str, Any], bundle: Path) -> None:
        if self.mlflow is None:
            return
        final = {
            "best_epoch": metadata["best_epoch"],
            "train_seconds": metadata["train_seconds"],
        }
        if metadata["best_dev_typed_f1"] is not None:
            final["best_dev_typed_f1"] = metadata["best_dev_typed_f1"]
        if metadata["peak_gpu_memory_mb"] is not None:
            final["peak_gpu_memory_mb"] = metadata["peak_gpu_memory_mb"]
        self.mlflow.log_metrics(final)
        self.mlflow.log_artifact(str(bundle / "metadata.json"))
        self.mlflow.end_run()
