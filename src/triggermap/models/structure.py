"""Document structure shared by the learners: which sentence or list a span belongs to.

Groups are flat and live within one sentence or one list (with its lead-in), so the group
classifiers only ever compare consecutive conditions that share a scope.
"""

from __future__ import annotations

from dataclasses import dataclass

from triggermap.text.markdown import BlockKind
from triggermap.text.preprocessing import PreprocessedDocument


@dataclass(frozen=True)
class Scope:
    kind: str  # "sentence", "list" or "none"
    key: int
    lead: str  # lead-in text of a list, "" otherwise

    def same(self, other: Scope) -> bool:
        return self.kind != "none" and (self.kind, self.key) == (other.kind, other.key)


def scope_of(doc: PreprocessedDocument, span: tuple[int, int]) -> Scope:
    for index, sentence in enumerate(doc.sentences):
        if sentence.start <= span[0] < sentence.end:
            block = doc.canonical.blocks[sentence.block]
            if block.kind is BlockKind.LIST_ITEM and block.list_id is not None:
                first = next(
                    i for i, b in enumerate(doc.canonical.blocks) if b.list_id == block.list_id
                )
                lead = ""
                if first > 0:
                    previous = doc.canonical.blocks[first - 1]
                    lead = doc.text[previous.start : previous.end]
                return Scope("list", block.list_id, lead)
            return Scope("sentence", index, "")
    return Scope("none", -1, "")


def context_for(doc: PreprocessedDocument, position: int) -> str:
    """Heading governing ``position`` and, inside a list, the list's lead-in paragraph."""
    blocks = doc.canonical.blocks
    containing = next((i for i, b in enumerate(blocks) if position < b.end), len(blocks) - 1)
    if containing < 0:
        return ""
    heading = next(
        (
            doc.text[b.start : b.end]
            for b in reversed(blocks[:containing])
            if b.kind is BlockKind.HEADING
        ),
        "",
    )
    lead = ""
    block = blocks[containing]
    if block.list_id is not None:
        first = next(i for i, b in enumerate(blocks) if b.list_id == block.list_id)
        if first > 0 and blocks[first - 1].kind is BlockKind.PARAGRAPH:
            lead = doc.text[blocks[first - 1].start : blocks[first - 1].end]
    return " — ".join(part for part in (heading, lead) if part)
