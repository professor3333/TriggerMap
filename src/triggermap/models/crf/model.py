"""CRF span tagger + logistic-regression category, role and group classifiers.

Pipeline per document: tokenise each sentence, tag condition boundaries with a linear-chain
CRF (B/I/O), classify each predicted span's category and role, then link consecutive
conditions in the same sentence or list into ALL/ANY/UNRESOLVED groups with a pairwise
classifier. Class weights are computed from training data only.

The saved bundle (a directory) holds the CRFsuite model, the pickled classifiers and a
metadata file with the feature and preprocessing versions and the training-data hash.
Bundles are produced by this project; never load one from an untrusted source.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pycrfsuite
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from triggermap.models.crf.features import (
    FEATURE_VERSION,
    Features,
    SentenceContext,
    pair_features,
    pos_tags,
    sentence_context,
    span_features,
    token_features,
)
from triggermap.models.crf.tokens import Token, bio_tags, spans_from_tags, tokenize
from triggermap.schema.models import (
    AdvisoryAnnotation,
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.markdown import BlockKind
from triggermap.text.preprocessing import PREPROCESSING_VERSION, PreprocessedDocument

NO_GROUP = "NONE"


class LabelClassifier:
    """Balanced logistic regression; degrades to a constant when training has one class."""

    def __init__(self, seed: int = 0) -> None:
        self.vectorizer = DictVectorizer()
        self.model = LogisticRegression(class_weight="balanced", max_iter=2000, random_state=seed)
        self.constant: str | None = None

    def fit(self, features: Sequence[Features], labels: Sequence[str]) -> LabelClassifier:
        classes = sorted(set(labels))
        if len(classes) <= 1:
            self.constant = classes[0] if classes else NO_GROUP
            return self
        self.model.fit(self.vectorizer.fit_transform(features), labels)
        return self

    def predict(self, features: Sequence[Features]) -> list[tuple[str, float]]:
        if not features:
            return []
        if self.constant is not None:
            return [(self.constant, 1.0)] * len(features)
        probabilities = self.model.predict_proba(self.vectorizer.transform(features))
        classes = list(self.model.classes_)
        return [(str(classes[row.argmax()]), float(row.max())) for row in probabilities]


@dataclass(frozen=True)
class _Unit:
    sentence_index: int
    tokens: list[Token]
    ctx: SentenceContext
    features: list[Features]


def _units(doc: PreprocessedDocument, use_pos: bool) -> list[_Unit]:
    units = []
    for index, sentence in enumerate(doc.sentences):
        tokens = tokenize(doc.text, sentence.start, sentence.end)
        if not tokens:
            continue
        ctx = sentence_context(doc, sentence)
        pos = pos_tags(doc.text, tokens, sentence.start) if use_pos else None
        units.append(_Unit(index, tokens, ctx, token_features(doc, tokens, ctx, pos)))
    return units


def _scope(doc: PreprocessedDocument, span: tuple[int, int]) -> tuple[str, int, str]:
    """(kind, id, lead-in text) of the sentence or list a condition belongs to."""
    for index, sentence in enumerate(doc.sentences):
        if sentence.start <= span[0] < sentence.end:
            block = doc.canonical.blocks[sentence.block]
            if block.kind is BlockKind.LIST_ITEM and block.list_id is not None:
                lead = ""
                first = next(
                    i for i, b in enumerate(doc.canonical.blocks) if b.list_id == block.list_id
                )
                if first > 0:
                    previous = doc.canonical.blocks[first - 1]
                    lead = doc.text[previous.start : previous.end]
                return "list", block.list_id, lead
            return "sentence", index, ""
    return "none", -1, ""


def _pairs(
    doc: PreprocessedDocument, spans: Sequence[tuple[int, int]]
) -> list[tuple[int, int, Features]]:
    """Consecutive condition pairs that share a sentence or list, with their features."""
    out: list[tuple[int, int, Features]] = []
    scopes = [_scope(doc, span) for span in spans]
    for i in range(len(spans) - 1):
        a, b = scopes[i], scopes[i + 1]
        if a[0] != "none" and a[:2] == b[:2]:
            feats = pair_features(doc.text, spans[i], spans[i + 1], a[0] == "list", a[2])
            out.append((i, i + 1, feats))
    return out


def training_hash(records: Sequence[AdvisoryAnnotation]) -> str:
    lines = sorted(r.model_dump_json() for r in records)
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


class CrfExtractor:
    def __init__(
        self,
        directory: Path,
        metadata: dict[str, Any],
        category: LabelClassifier,
        role: LabelClassifier,
        group: LabelClassifier,
    ) -> None:
        self.directory = directory
        self.metadata = metadata
        self.model_id = str(metadata["model_id"])
        self.use_pos = bool(metadata["use_pos"])
        self.category = category
        self.role = role
        self.group = group
        self._tagger = pycrfsuite.Tagger()
        self._tagger.open(str(directory / "tagger.crfsuite"))

    # -- training

    @classmethod
    def train(
        cls,
        examples: Sequence[tuple[PreprocessedDocument, AdvisoryAnnotation]],
        out_dir: Path,
        *,
        model_id: str = "crf-1",
        use_pos: bool = True,
        c1: float = 0.1,
        c2: float = 0.1,
        max_iterations: int = 200,
        seed: int = 0,
    ) -> CrfExtractor:
        out_dir.mkdir(parents=True, exist_ok=True)
        trainer = pycrfsuite.Trainer(verbose=False)
        span_x: list[Features] = []
        category_y: list[str] = []
        role_y: list[str] = []
        pair_x: list[Features] = []
        pair_y: list[str] = []
        stats: Counter[str] = Counter()

        for doc, record in examples:
            if record.content_hash != doc.content_hash:
                raise ValueError(f"{record.advisory_id}: annotation is for different text")
            conditions = sorted(record.conditions, key=lambda c: c.span)
            placed: set[str] = set()
            for unit in _units(doc, use_pos):
                sentence = doc.sentences[unit.sentence_index]
                inside = [
                    c
                    for c in conditions
                    if sentence.start <= c.span[0] and c.span[1] <= sentence.end
                ]
                tags, unreachable = bio_tags(unit.tokens, [c.span for c in inside])
                trainer.append(unit.features, tags)
                stats["sentences"] += 1
                stats["tokens"] += len(unit.tokens)
                stats["unreachable_spans"] += len(unreachable)
                starts = {t.start: i for i, t in enumerate(unit.tokens)}
                ends = {t.end: i for i, t in enumerate(unit.tokens)}
                for cond in inside:
                    placed.add(cond.id)
                    if cond.span[0] in starts and cond.span[1] in ends:
                        first, last = starts[cond.span[0]], ends[cond.span[1]]
                        in_code = doc.canonical.in_code(cond.span[0])
                        span_x.append(span_features(unit.tokens, first, last, unit.ctx, in_code))
                        category_y.append(cond.category.value)
                        role_y.append(cond.role.value)
            stats["gold_spans"] += len(conditions)
            stats["unreachable_spans"] += len([c for c in conditions if c.id not in placed])

            group_of = {m: g.operator.value for g in record.groups for m in g.members}
            group_index = {m: i for i, g in enumerate(record.groups) for m in g.members}
            for i, j, feats in _pairs(doc, [c.span for c in conditions]):
                a, b = conditions[i].id, conditions[j].id
                same = a in group_index and group_index.get(a) == group_index.get(b)
                pair_x.append(feats)
                pair_y.append(group_of[a] if same else NO_GROUP)

        trainer.set_params(
            {
                "c1": c1,
                "c2": c2,
                "max_iterations": max_iterations,
                "feature.possible_transitions": True,
            }
        )
        trainer.train(str(out_dir / "tagger.crfsuite"))
        category = LabelClassifier(seed).fit(span_x, category_y)
        role = LabelClassifier(seed).fit(span_x, role_y)
        group = LabelClassifier(seed).fit(pair_x, pair_y)
        joblib.dump(
            {"category": category, "role": role, "group": group}, out_dir / "classifiers.joblib"
        )

        records = [record for _, record in examples]
        metadata = {
            "model_id": model_id,
            "family": "crf",
            "feature_version": FEATURE_VERSION,
            "preprocessing_version": PREPROCESSING_VERSION,
            "use_pos": use_pos,
            "hyperparameters": {"c1": c1, "c2": c2, "max_iterations": max_iterations, "seed": seed},
            "training_documents": len(records),
            "training_hash": training_hash(records),
            "stats": dict(stats),
            "label_counts": {
                "category": dict(Counter(category_y)),
                "role": dict(Counter(role_y)),
                "group_pairs": dict(Counter(pair_y)),
            },
        }
        (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True))
        return cls(out_dir, metadata, category, role, group)

    @classmethod
    def load(cls, directory: Path) -> CrfExtractor:
        metadata = json.loads((directory / "metadata.json").read_text())
        if metadata["preprocessing_version"] != PREPROCESSING_VERSION:
            raise ValueError(
                f"bundle built for preprocessing {metadata['preprocessing_version']}, "
                f"running {PREPROCESSING_VERSION}"
            )
        classifiers = joblib.load(directory / "classifiers.joblib")
        return cls(
            directory, metadata, classifiers["category"], classifiers["role"], classifiers["group"]
        )

    # -- inference

    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction:
        found: list[tuple[tuple[int, int], Features, float]] = []
        for unit in _units(doc, self.use_pos):
            tags = self._tagger.tag(unit.features)
            for first, stop in spans_from_tags(unit.tokens, tags):
                marginals = [self._marginal(tags[i], i) for i in range(first, stop)]
                span = (unit.tokens[first].start, unit.tokens[stop - 1].end)
                in_code = doc.canonical.in_code(span[0])
                feats = span_features(unit.tokens, first, stop - 1, unit.ctx, in_code)
                found.append((span, feats, min(marginals)))

        categories = self.category.predict([f for _, f, _ in found])
        roles = self.role.predict([f for _, f, _ in found])
        conditions = [
            Condition(
                id=f"c{i + 1}",
                span=span,
                category=Category(category),
                role=Role(role),
                source="model",
                confidence=round(span_conf * role_conf, 4),
            )
            for i, ((span, _, span_conf), (category, _), (role, role_conf)) in enumerate(
                zip(found, categories, roles, strict=True)
            )
        ]
        groups = self._groups(doc, conditions)
        flags = [f"low_confidence:{c.id}" for c in conditions if (c.confidence or 0) < 0.5]
        flags += ["unresolved_group" for g in groups if g.operator is GroupOperator.UNRESOLVED]
        return Extraction(
            advisory_id=advisory_id,
            content_hash=doc.content_hash,
            preprocessing_version=doc.version,
            model_id=self.model_id,
            document_status=(
                DocumentStatus.HAS_CONDITIONS
                if conditions
                else DocumentStatus.NO_EXPLICIT_CONDITION
            ),
            conditions=tuple(conditions),
            groups=tuple(groups),
            review_flags=tuple(flags),
        )

    def _marginal(self, tag: str, index: int) -> float:
        try:
            return float(self._tagger.marginal(tag, index))
        except ValueError:  # label never seen in training
            return 0.0

    def _groups(self, doc: PreprocessedDocument, conditions: Sequence[Condition]) -> list[Group]:
        pairs = _pairs(doc, [c.span for c in conditions])
        labels = self.group.predict([feats for _, _, feats in pairs])
        chains: list[tuple[list[int], set[str]]] = []
        for (i, j, _), (label, _) in zip(pairs, labels, strict=True):
            if label == NO_GROUP:
                continue
            if chains and chains[-1][0][-1] == i:
                chains[-1][0].append(j)
                chains[-1][1].add(label)
            else:
                chains.append(([i, j], {label}))
        return [
            Group(
                operator=GroupOperator(next(iter(ops)))
                if len(ops) == 1
                else GroupOperator.UNRESOLVED,
                members=tuple(conditions[k].id for k in members),
            )
            for members, ops in chains
        ]
