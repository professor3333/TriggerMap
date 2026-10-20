"""Surface cues that suggest an advisory states conditions.

Used only for corpus statistics and for enriching the *training* sample with
condition-rich candidates. Cues are never labels and never decide evaluation membership.
"""

from __future__ import annotations

import re

CUE_GROUPS: dict[str, tuple[str, ...]] = {
    "conditional": (
        r"when",
        r"if",
        r"unless",
        r"only (?:if|when)",
        r"provided that",
        r"as long as",
        r"in case",
        r"whenever",
    ),
    "requirement": (
        r"requires?",
        r"required",
        r"must",
        r"needs? to",
        r"necessary",
        r"prerequisites?",
        r"conditions? (?:are|is) met",
    ),
    "configuration": (
        r"enabled?",
        r"disabled?",
        r"configur(?:ed|ation)",
        r"options?",
        r"settings?",
        r"flags?",
        r"by default",
        r"set to",
    ),
    "access": (
        r"(?:un)?authenticated",
        r"privileg(?:e|es|ed)",
        r"admin(?:istrator)?s?",
        r"logged[- ]in",
        r"local (?:access|user|attacker)s?",
        r"remote(?:ly)? (?:attacker|user)s?",
        r"valid (?:account|credentials|session)",
    ),
    "exception": (
        r"not (?:vulnerable|affected|required|needed)",
        r"unaffected",
        r"need not",
        r"except(?:ion)?",
        r"regardless",
        r"even (?:if|when|without)",
    ),
}

_PATTERNS = {
    group: re.compile(r"\b(?:" + "|".join(cues) + r")\b", re.IGNORECASE)
    for group, cues in CUE_GROUPS.items()
}


def cue_counts(text: str) -> dict[str, int]:
    return {group: len(pattern.findall(text)) for group, pattern in _PATTERNS.items()}


def condition_score(text: str) -> int:
    """Distinct cue groups present, plus conditional cues (capped) as a tie-breaker."""
    counts = cue_counts(text)
    return sum(1 for n in counts.values() if n) + min(counts["conditional"], 5)
