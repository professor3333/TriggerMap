"""Rules baseline: conditional clauses, list scope, exceptions and explicit non-requirements.

The baseline is tuned for precision. A conditional clause becomes a condition only when it
contains a deployment cue (configuration, usage, access or platform vocabulary), because
most "when …" clauses in advisories describe the bug's mechanism, not the deployment.
Sections about workarounds, fixes, proofs of concept and credits are skipped.

Confidences are fixed per rule. They order predictions for precision-coverage analysis
but are not calibrated probabilities.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass

from triggermap.schema.models import (
    Category,
    Condition,
    DocumentStatus,
    Extraction,
    Group,
    GroupOperator,
    Role,
)
from triggermap.text.markdown import Block, BlockKind
from triggermap.text.preprocessing import PreprocessedDocument
from triggermap.text.segment import Sentence

MODEL_ID = "rules-1"

_SKIP_SECTION = re.compile(
    r"workaround|mitigat|remediat|patch|\bfix|resolution|credit|acknowledg|reference|timeline|"
    r"disclosure|proof of concept|\bpoc\b|reproduc|steps to|exploit|recommend|suggest|solution|"
    r"resource|thank",
    re.IGNORECASE,
)
_IMPERATIVE = re.compile(
    r"(?:upgrade|update|disable|enable|set|avoid|do not|don't|never|users should|you should|"
    r"we recommend|it is recommended|to mitigate|as a workaround|consider|ensure|make sure)\b",
    re.IGNORECASE,
)
_NOT_A_CONDITION = re.compile(
    r"^(?:successful|exploited|successfully exploited|an attacker succeeds|so|not|true|false)\b",
    re.IGNORECASE,
)

_ACCESS = re.compile(
    r"authenticat|\bprivileg|\badmin|logged[- ]in|permission|\baccount\b|credential|"
    r"\battacker\b|\brole\b|\baccess to\b|\blocal user|\bremote user",
    re.IGNORECASE,
)
_CONFIGURATION = re.compile(
    r"\benabled?\b|\bdisabled?\b|\bset to\b|=|\boption\b|\bsetting|\bflag\b|\bconfig|"
    r"\bdefault\b|\btrue\b|\bfalse\b|environment variable|\bparameter\b|\bargument\b",
    re.IGNORECASE,
)
_PLATFORM = re.compile(
    r"\bwindows\b|\blinux\b|\bmacos\b|\bpython (?:\d|version)|operating system|\bproxy\b|"
    r"\bbehind\b|\bdocker\b|kubernetes|file ?system|\bnginx\b|\bapache\b|\bgpu\b|\bcpu\b|"
    r"32-bit|64-bit|\bhost(?:ed)?\b|symlink",
    re.IGNORECASE,
)
_USAGE = re.compile(
    r"\busing\b|\buses?\b|\bused\b|\bcall(?:s|ed|ing)?\b|\bconfigured\b|\bdeploy|\brun(?:s|ning)?\b|"
    r"\bexpos|\bserv(?:e|es|ed|ing)\b|\binstall|\bload(?:s|ed|ing)?\b|\bpass(?:es|ed|ing)?\b|"
    r"\bprocess(?:es|ed|ing)?\b|\brender|\bpars(?:e|es|ed|ing)\b|\baccept|\ballow(?:s|ed)?\b|"
    r"\benabling\b",
    re.IGNORECASE,
)

# "regardless of if …" and "even when …" introduce non-requirements, handled separately.
_CONDITIONAL = re.compile(
    r"(?<!regardless of )(?<!regardless of whether )(?<!even )"
    r"\b(?P<cue>only (?:if|when)|when(?:ever)?|if|as long as|provided that|in case)\s+",
    re.IGNORECASE,
)
_UNLESS = re.compile(r"\b(?:unless|except (?:when|if))\s+", re.IGNORECASE)
_NOT_AFFECTED = re.compile(
    r"\b(?:not (?:affected|vulnerable|exploitable)|unaffected|safe)\s+(?:if|when|unless)\s+",
    re.IGNORECASE,
)
_ONLY_AFFECTS = re.compile(
    r"\b(?:only (?:affects|applies to|impacts)|affects only|is only (?:exploitable|vulnerable) "
    r"(?:when|if)|only (?:exploitable|vulnerable) (?:when|if))\s+",
    re.IGNORECASE,
)
_REQUIRES = re.compile(
    r"\b(?:exploitation|exploiting this|the attack|this attack|the vulnerability|"
    r"this vulnerability)\s+requires?\s+(?:that\s+)?",
    re.IGNORECASE,
)
_REGARDLESS = re.compile(r"\bregardless of (?:whether |if )?", re.IGNORECASE)
_EVEN_NOT = re.compile(
    r"\beven (?:when|if)\s+(?P<x>[^,.;:]+?)\s+(?:is|are)\s+not\s+"
    r"(?:present|enabled|used|configured|set|installed|exposed)\b",
    re.IGNORECASE,
)
_NO_AUTH = re.compile(
    r"\b(?:without (?:requiring |any )?(?P<a>authentication)|"
    r"no (?P<b>authentication) (?:is )?required|"
    r"does not require (?P<c>authentication)|(?P<d>unauthenticated))\b",
    re.IGNORECASE,
)
_AUTH_ACTOR = re.compile(
    r"\b(?:an?|any)\s+(?P<x>(?:authenticated|logged[- ]in|privileged|admin(?:istrator)?)\s+"
    r"(?:remote\s+)?(?:attacker|user|account)s?(?:\s+with\s+[\w\s-]{1,40}?"
    r"(?:permission|privileges?|role|access)s?)?|(?:attacker|user)s?\s+with\s+[\w\s-]{1,40}?"
    r"(?:permission|privileges?|role|access)s?)\b",
    re.IGNORECASE,
)
_CONFIG_INLINE = re.compile(
    r"\b(?P<x>[A-Za-z_][\w.]*_[\w.]*\s*(?:=|==|\bset to\b|\bis set to\b)\s*"
    r"(?:True|False|true|false|None|\d+|\"[^\"]*\"|'[^']*'))",
)

_LEAD_IN = re.compile(
    r"following|conditions?|only (?:if|when|for|affects)|affected (?:if|when)|"
    r"vulnerable (?:if|when)|requires?|prerequisite|must|combine",
    re.IGNORECASE,
)
_ALL = re.compile(r"\ball (?:of )?(?:the following|these|conditions)|\bcombine|\bboth\b", re.I)
_ANY = re.compile(r"\b(?:any|one) of (?:the following|these)|\beither\b", re.IGNORECASE)
_NEGATIVE_LEAD = re.compile(r"not affected|unaffected|not vulnerable|unless|except", re.I)

_SUBJECT = re.compile(
    r"(?:(?:the|an?|your|any)\s+)?(?:application|app|server|service|user|developer|deployment|"
    r"instance|project|program|code|system|website|site)s?\s+(?:must\s+be\s+|must\s+|also\s+)?",
    re.IGNORECASE,
)
_CLAUSE_END = re.compile(
    r",|;|:|\.\s|\.$|\s(?:then|it|this|which|an attacker|attackers)\s|"
    r"\s(?:can|could|may|might|will|would|leads?|results?|allows?|causes?|enables?)\s",
    re.IGNORECASE,
)
_WORD = re.compile(r"[A-Za-z][\w.]{1,}")
_SPLIT_CONJ = re.compile(
    r"\s+(?P<op>and|or)\s+(?=(?:\w+ing|the|an?|its|when|if|\w+_\w+)\b)", re.IGNORECASE
)
_LEADING_CUE = re.compile(r"(?:when(?:ever)?|if|only (?:if|when))\s+", re.IGNORECASE)
_SPLIT_WITH = re.compile(r"\s+with\s+(?=[\w.'\"]+\s*(?:=|set to|enabled|disabled))", re.I)


@dataclass(frozen=True)
class _Candidate:
    start: int
    end: int
    category: Category
    role: Role
    confidence: float
    clause: int | None = None  # candidates from one clause or list may be grouped
    operator: GroupOperator | None = None


def categorize(text: str) -> Category:
    if _ACCESS.search(text):
        return Category.ACCESS
    if _CONFIGURATION.search(text):
        return Category.CONFIGURATION
    if _PLATFORM.search(text):
        return Category.PLATFORM
    return Category.USAGE


def _has_deployment_cue(text: str) -> bool:
    return any(p.search(text) for p in (_ACCESS, _CONFIGURATION, _PLATFORM, _USAGE))


def _clean(text: str, start: int, end: int) -> tuple[int, int] | None:
    """Trim cue-free subjects, punctuation and dangling conjunctions; None if nothing left."""
    while True:
        before = (start, end)
        while start < end and (
            text[start].isspace()
            or text[start] == "("
            or (text[start] in "\"'" and text[start:end].count(text[start]) % 2 == 1)
        ):
            start += 1
        while end > start and (text[end - 1].isspace() or text[end - 1] in ".,;:!?"):
            end -= 1
        for prefix in (_LEADING_CUE, _SUBJECT):
            m = prefix.match(text, start, end)
            if m and m.end() < end:
                start = m.end()
        for tail in (" and", " or", " and/or"):
            if text[start:end].lower().endswith(tail):
                end -= len(tail)
        if end > start and text[end - 1] == ")":
            if "(" not in text[start:end]:
                end -= 1  # stray closer from an enclosing parenthetical
            elif (open_index := text.rindex("(", start, end)) > start:
                end = open_index
        if end > start and text[end - 1] in "\"'" and text[start:end].count(text[end - 1]) % 2:
            end -= 1
        if (start, end) == before:
            break
    if end - start < 3 or end - start > 200:
        return None
    return start, end


class RuleExtractor:
    model_id = MODEL_ID

    def extract(self, doc: PreprocessedDocument, advisory_id: str | None = None) -> Extraction:
        candidates = list(self._candidates(doc))
        conditions, groups = _resolve(candidates)
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

    # -- candidate generation

    def _candidates(self, doc: PreprocessedDocument) -> Iterator[_Candidate]:
        text = doc.text
        blocks = doc.canonical.blocks
        skip_blocks = _skipped_blocks(text, blocks)
        clause_id = 0
        for sentence in doc.sentences:
            block = blocks[sentence.block]
            if sentence.block in skip_blocks or block.kind in (BlockKind.CODE, BlockKind.HEADING):
                continue
            if _IMPERATIVE.match(text, sentence.start, sentence.end):
                continue
            yield from self._sentence(text, sentence, clause_id)
            clause_id += 10_000
        yield from self._lists(text, blocks, doc.sentences, skip_blocks, clause_id)

    def _sentence(self, text: str, s: Sentence, clause_base: int) -> Iterator[_Candidate]:
        clause_id = clause_base
        for pattern, role, confidence in (
            (_ONLY_AFFECTS, Role.REQUIRED, 0.75),
            (_REQUIRES, Role.REQUIRED, 0.6),
            (_NOT_AFFECTED, Role.EXCEPTION, 0.6),
            (_UNLESS, Role.EXCEPTION, 0.6),
            (_CONDITIONAL, Role.REQUIRED, 0.55),
        ):
            for m in pattern.finditer(text, s.start, s.end):
                clause_id += 1
                yield from self._clause(text, m.end(), s.end, role, confidence, clause_id)

        for m in _EVEN_NOT.finditer(text, s.start, s.end):
            span = _clean(text, m.start("x"), m.end("x"))
            if span:
                yield _Candidate(*span, categorize(text[slice(*span)]), Role.NOT_REQUIRED, 0.6)
        for m in _REGARDLESS.finditer(text, s.start, s.end):
            end = _clause_end(text, m.end(), s.end)
            span = _clean(text, m.end(), end)
            if span:
                yield _Candidate(*span, categorize(text[slice(*span)]), Role.NOT_REQUIRED, 0.55)
        for m in _NO_AUTH.finditer(text, s.start, s.end):
            group = next(g for g in ("a", "b", "c", "d") if m.group(g))
            yield _Candidate(m.start(group), m.end(group), Category.ACCESS, Role.NOT_REQUIRED, 0.6)
        for m in _AUTH_ACTOR.finditer(text, s.start, s.end):
            if not re.match(r"un", m.group("x"), re.I):
                yield _Candidate(m.start("x"), m.end("x"), Category.ACCESS, Role.REQUIRED, 0.6)
        for m in _CONFIG_INLINE.finditer(text, s.start, s.end):
            yield _Candidate(m.start("x"), m.end("x"), Category.CONFIGURATION, Role.REQUIRED, 0.35)

    def _clause(
        self, text: str, start: int, limit: int, role: Role, confidence: float, clause_id: int
    ) -> Iterator[_Candidate]:
        end = _clause_end(text, start, limit)
        clause = text[start:end]
        if _NOT_A_CONDITION.match(clause) or not _has_deployment_cue(clause):
            return
        pieces: list[tuple[int, int]] = []
        operator: GroupOperator | None = None
        cursor = start
        for m in _split_points(text, start, end):
            pieces.append((cursor, m[0]))
            cursor = m[1]
            op = m[2]
            operator = op if operator in (None, op) else GroupOperator.UNRESOLVED
        pieces.append((cursor, end))
        for piece_start, piece_end in pieces:
            span = _clean(text, piece_start, piece_end)
            if span is None:
                continue
            surface = text[slice(*span)]
            if _NOT_A_CONDITION.match(surface) or len(_WORD.findall(surface)) < 2:
                continue
            yield _Candidate(
                *span,
                categorize(surface),
                role,
                confidence if _has_deployment_cue(surface) else confidence - 0.15,
                clause_id if len(pieces) > 1 else None,
                operator if len(pieces) > 1 else None,
            )

    def _lists(
        self,
        text: str,
        blocks: tuple[Block, ...],
        sentences: tuple[Sentence, ...],
        skip_blocks: set[int],
        clause_base: int,
    ) -> Iterator[_Candidate]:
        clause_id = clause_base
        for index, block in enumerate(blocks):
            if block.kind is not BlockKind.LIST_ITEM or index in skip_blocks:
                continue
            first_in_list = index == 0 or blocks[index - 1].list_id != block.list_id
            if not first_in_list or index == 0:
                continue
            lead = blocks[index - 1]
            if lead.kind is not BlockKind.PARAGRAPH:
                continue
            lead_sentences = [s for s in sentences if s.block == index - 1]
            if not lead_sentences:
                continue
            lead_text = text[lead_sentences[-1].start : lead_sentences[-1].end]
            introduces_list = lead_text.rstrip().endswith(":") or _ALL.search(lead_text)
            if not introduces_list or not _LEAD_IN.search(lead_text):
                continue
            items = [
                b
                for b in blocks[index:]
                if b.kind is BlockKind.LIST_ITEM and b.list_id == block.list_id and b.level == 0
            ]
            operator = _list_operator(lead_text, [text[b.start : b.end] for b in items])
            role = Role.EXCEPTION if _NEGATIVE_LEAD.search(lead_text) else Role.REQUIRED
            clause_id += 1
            for item in items:
                span = _clean(text, item.start, item.end)
                if span is None:
                    continue
                yield _Candidate(
                    *span,
                    categorize(text[slice(*span)]),
                    role,
                    0.75,
                    clause_id if len(items) > 1 else None,
                    operator if len(items) > 1 else None,
                )


def _list_operator(lead_text: str, items: list[str]) -> GroupOperator:
    """Logic of a lead-in list: from the lead-in, else from "; and" / "; or" item endings."""
    endings = {item.rstrip(" ;,.").rsplit(None, 1)[-1].lower() for item in items[:-1] if item}
    if _ANY.search(lead_text) or "or" in endings:
        return GroupOperator.ANY
    if _ALL.search(lead_text) or "and" in endings:
        return GroupOperator.ALL
    return GroupOperator.UNRESOLVED


def _clause_end(text: str, start: int, limit: int) -> int:
    m = _CLAUSE_END.search(text, start, limit)
    return m.start() if m else limit


def _split_points(text: str, start: int, end: int) -> Iterator[tuple[int, int, GroupOperator]]:
    points: list[tuple[int, int, GroupOperator]] = []
    for m in _SPLIT_CONJ.finditer(text, start, end):
        op = GroupOperator.ALL if m.group("op").lower() == "and" else GroupOperator.ANY
        points.append((m.start(), m.end(), op))
    for m in _SPLIT_WITH.finditer(text, start, end):
        points.append((m.start(), m.end(), GroupOperator.ALL))
    yield from sorted(points)


def _skipped_blocks(text: str, blocks: tuple[Block, ...]) -> set[int]:
    skipped: set[int] = set()
    skipping = False
    for index, block in enumerate(blocks):
        if block.kind is BlockKind.HEADING:
            skipping = bool(_SKIP_SECTION.search(text[block.start : block.end]))
        elif skipping:
            skipped.add(index)
    return skipped


def _resolve(candidates: list[_Candidate]) -> tuple[list[Condition], list[Group]]:
    """Keep the most confident non-overlapping candidates, then rebuild groups."""
    chosen: list[_Candidate] = []
    for cand in sorted(candidates, key=lambda c: (-c.confidence, -(c.end - c.start), c.start)):
        if all(cand.end <= o.start or cand.start >= o.end for o in chosen):
            chosen.append(cand)
    chosen.sort(key=lambda c: (c.start, c.end))
    conditions = [
        Condition(
            id=f"c{i + 1}",
            span=(c.start, c.end),
            category=c.category,
            role=c.role,
            source="rules",
            confidence=round(c.confidence, 3),
        )
        for i, c in enumerate(chosen)
    ]
    members: dict[int, list[str]] = {}
    operators: dict[int, GroupOperator] = {}
    for cand, cond in zip(chosen, conditions, strict=True):
        if cand.clause is not None and cand.operator is not None:
            members.setdefault(cand.clause, []).append(cond.id)
            operators[cand.clause] = cand.operator
    groups = [
        Group(operator=operators[key], members=tuple(ids))
        for key, ids in sorted(members.items(), key=lambda kv: kv[1][0])
        if len(ids) >= 2
    ]
    groups.sort(key=lambda g: int(g.members[0][1:]))
    return conditions, groups
