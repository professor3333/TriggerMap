"""Advisory Markdown → canonical text, with a per-character map back to the raw text.

Canonical text is the raw text with display markup removed (heading and list markers,
emphasis delimiters, backticks, link targets, formatting tags), LF line endings, soft
line breaks joined with a space, and NFC applied to prose only. Code (inline and block)
is copied verbatim. Every canonical character records the raw range it came from, so
any canonical span maps back to raw offsets.

Layout of the canonical text: one line per heading, paragraph, list item, table row or
code line. Blocks are separated by "\\n", or "\\n\\n" when the source had a blank line.

Markup removal is best-effort: anything the parser does not recognise is kept as
literal text, which costs some noise but never breaks the offset map.
"""

from __future__ import annotations

import html
import re
import string
import unicodedata
from dataclasses import dataclass, field
from enum import StrEnum

# (character, raw_start, raw_end): one canonical character and the raw range it came from.
Item = tuple[str, int, int]


class BlockKind(StrEnum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    CODE = "code"
    TABLE = "table"
    QUOTE = "quote"


@dataclass(frozen=True)
class Block:
    kind: BlockKind
    start: int
    end: int
    level: int = 0  # heading level, or nesting depth for list items
    list_id: int | None = None  # shared by every item (and nested code) of one list
    ordered: bool = False


@dataclass(frozen=True)
class CanonicalText:
    raw: str
    text: str
    raw_starts: tuple[int, ...]
    raw_ends: tuple[int, ...]
    blocks: tuple[Block, ...]
    code_spans: tuple[tuple[int, int], ...]  # inline code and code blocks, canonical offsets

    def to_raw(self, start: int, end: int) -> tuple[int, int]:
        """Map a half-open canonical span to the half-open raw span it came from."""
        if not 0 <= start < end <= len(self.text):
            raise ValueError(f"invalid canonical span [{start}, {end}) for length {len(self.text)}")
        return self.raw_starts[start], self.raw_ends[end - 1]

    def in_code(self, index: int) -> bool:
        return any(start <= index < end for start, end in self.code_spans)


# ---------------------------------------------------------------------------
# Lines


@dataclass(frozen=True)
class _Line:
    text: str
    start: int  # raw offset of the first character
    term: tuple[int, int]  # raw range of the line terminator (empty at end of input)

    def items(self, begin: int = 0, end: int | None = None) -> list[Item]:
        stop = len(self.text) if end is None else end
        return [(self.text[i], self.start + i, self.start + i + 1) for i in range(begin, stop)]


_NEWLINE = re.compile(r"\r\n|\r|\n")


def _split_lines(raw: str) -> list[_Line]:
    lines: list[_Line] = []
    pos = 0
    for m in _NEWLINE.finditer(raw):
        lines.append(_Line(raw[pos : m.start()], pos, (m.start(), m.end())))
        pos = m.end()
    if pos < len(raw):
        lines.append(_Line(raw[pos:], pos, (len(raw), len(raw))))
    return lines


def _indent(text: str) -> int:
    width = 0
    for ch in text:
        if ch == " ":
            width += 1
        elif ch == "\t":
            width += 4 - width % 4
        else:
            break
    return width


def _blank(text: str) -> bool:
    return not text.strip()


# ---------------------------------------------------------------------------
# Block structure

_FENCE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
_ATX = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$")
_HR = re.compile(r"^ {0,3}(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$")
_SETEXT = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
_LIST = re.compile(r"^([ \t]*)([-*+]|\d{1,9}[.)])([ \t]+|$)")
_QUOTE = re.compile(r"^ {0,3}> ?")
_LINK_DEF = re.compile(r"^ {0,3}\[[^\]]+\]:[ \t]*\S+")
_TABLE_DELIM = re.compile(r"^[ \t]*\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$")


@dataclass
class _RawBlock:
    kind: BlockKind
    lines: list[list[Item]]  # logical lines; prose lines are inline-processed later
    joins: list[Item]  # separator item placed before each logical line after the first
    last_term: tuple[int, int]
    gap: tuple[int, int] | None = None  # terminator of the first blank line before the block
    level: int = 0
    list_id: int | None = None
    ordered: bool = False
    verbatim: bool = False


@dataclass
class _Parser:
    lines: list[_Line]
    i: int = 0
    blocks: list[_RawBlock] = field(default_factory=list)
    gap: tuple[int, int] | None = None
    next_list_id: int = 0

    def run(self) -> list[_RawBlock]:
        while self.i < len(self.lines):
            self._block()
        return self.blocks

    # -- helpers

    def _peek(self, offset: int = 0) -> _Line | None:
        j = self.i + offset
        return self.lines[j] if j < len(self.lines) else None

    def _emit(self, block: _RawBlock) -> None:
        block.gap = self.gap
        self.gap = None
        self.blocks.append(block)

    def _mark_gap(self, line: _Line) -> None:
        if self.gap is None:
            self.gap = line.term

    def _starts_block(self, text: str) -> bool:
        if _FENCE.match(text) and _indent(text) < 4:
            return True
        if _ATX.match(text) or _HR.match(text) or _QUOTE.match(text):
            return True
        if text.lstrip().startswith("<!--"):
            return True
        m = _LIST.match(text)
        return m is not None and not _blank(text[m.end() :])

    # -- dispatch

    def _block(self) -> None:
        line = self.lines[self.i]
        text = line.text
        if _blank(text):
            self._mark_gap(line)
            self.i += 1
        elif _FENCE.match(text) and _indent(text) < 4:
            self._emit(self._fenced_code())
        elif m := _ATX.match(text):
            self.i += 1
            if m.group(2) is None:
                return
            items = line.items(m.start(2), m.end(2))
            self._emit(_RawBlock(BlockKind.HEADING, [items], [], line.term, level=len(m.group(1))))
        elif _HR.match(text):
            self._mark_gap(line)
            self.i += 1
        elif text.lstrip().startswith("<!--"):
            self._html_comment()
        elif _LINK_DEF.match(text):
            self._mark_gap(line)
            self.i += 1
        elif self._table_start():
            self._emit(self._table())
        elif _QUOTE.match(text):
            self._emit(self._quote())
        elif _LIST.match(text):
            self._list()
        elif _indent(text) >= 4:
            self._emit(self._indented_code())
        else:
            self._emit(self._paragraph())

    # -- leaf blocks

    def _fenced_code(self) -> _RawBlock:
        opener = self.lines[self.i]
        m = _FENCE.match(opener.text)
        assert m is not None
        indent, fence = _indent(m.group(1)), m.group(2)
        closer = re.compile(rf"^[ \t]*{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$")
        self.i += 1
        body: list[_Line] = []
        last_term = opener.term
        while self.i < len(self.lines):
            line = self.lines[self.i]
            self.i += 1
            last_term = line.term
            if closer.match(line.text):
                break
            body.append(line)
        return self._code_block(body, indent, last_term)

    def _indented_code(self) -> _RawBlock:
        body: list[_Line] = []
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if _blank(line.text):
                nxt = self._next_nonblank()
                if nxt is None or _indent(nxt.text) < 4:
                    break
            elif _indent(line.text) < 4:
                break
            body.append(line)
            self.i += 1
        return self._code_block(body, 4, body[-1].term)

    def _code_block(self, body: list[_Line], strip: int, last_term: tuple[int, int]) -> _RawBlock:
        lines: list[list[Item]] = []
        joins: list[Item] = []
        for index, line in enumerate(body):
            cut = 0
            while cut < len(line.text) and cut < strip and line.text[cut] == " ":
                cut += 1
            if index:
                joins.append(("\n", *body[index - 1].term))
            lines.append(line.items(cut))
        return _RawBlock(BlockKind.CODE, lines, joins, last_term, verbatim=True)

    def _next_nonblank(self) -> _Line | None:
        j = self.i
        while j < len(self.lines) and _blank(self.lines[j].text):
            j += 1
        return self.lines[j] if j < len(self.lines) else None

    def _html_comment(self) -> None:
        while self.i < len(self.lines):
            line = self.lines[self.i]
            self.i += 1
            if "-->" in line.text:
                self._mark_gap(line)
                return

    def _table_start(self) -> bool:
        nxt = self._peek(1)
        return (
            "|" in self.lines[self.i].text
            and nxt is not None
            and "-" in nxt.text
            and bool(_TABLE_DELIM.match(nxt.text))
        )

    def _table(self) -> _RawBlock:
        rows: list[_Line] = [self.lines[self.i]]
        self.i += 2  # header and delimiter row
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if _blank(line.text) or "|" not in line.text:
                break
            rows.append(line)
            self.i += 1
        lines: list[list[Item]] = []
        joins: list[Item] = []
        for index, row in enumerate(rows):
            begin, end = 0, len(row.text)
            while begin < end and row.text[begin] in " \t":
                begin += 1
            while end > begin and row.text[end - 1] in " \t":
                end -= 1
            if begin < end and row.text[begin] == "|":
                begin += 1
            if end > begin and row.text[end - 1] == "|" and row.text[end - 2 : end] != "\\|":
                end -= 1
            if index:
                joins.append(("\n", *rows[index - 1].term))
            lines.append(row.items(begin, end))
        return _RawBlock(BlockKind.TABLE, lines, joins, rows[-1].term)

    def _quote(self) -> _RawBlock:
        body: list[list[Item]] = [[]]
        joins: list[Item] = []
        last = self.lines[self.i]
        while self.i < len(self.lines):
            line = self.lines[self.i]
            m = _QUOTE.match(line.text)
            if m is None:
                break
            content = line.items(m.end())
            if _blank(line.text[m.end() :]):
                if body[-1]:
                    joins.append(("\n", *line.term))
                    body.append([])
            else:
                if body[-1]:
                    _soft_break(body[-1], last.term)
                body[-1].extend(_lstrip(content))
            last = line
            self.i += 1
        lines = [b for b in body if b]
        return _RawBlock(BlockKind.QUOTE, lines, joins[: max(len(lines) - 1, 0)], last.term)

    def _paragraph(self) -> _RawBlock:
        first = self.lines[self.i]
        content = _lstrip(first.items())
        last = first
        self.i += 1
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if _blank(line.text):
                break
            if _SETEXT.match(line.text):
                level = 1 if line.text.strip().startswith("=") else 2
                self.i += 1
                _rstrip(content)
                return _RawBlock(BlockKind.HEADING, [content], [], line.term, level=level)
            if self._starts_block(line.text) or self._table_start():
                break
            _soft_break(content, last.term)
            content.extend(_lstrip(line.items()))
            last = line
            self.i += 1
        return _RawBlock(BlockKind.PARAGRAPH, [content], [], last.term)

    # -- lists

    def _list(self) -> None:
        list_id = self.next_list_id
        self.next_list_id += 1
        stack: list[int] = []
        item: _RawBlock | None = None
        content_indent = 0
        blank_seen: _Line | None = None

        while self.i < len(self.lines):
            line = self.lines[self.i]
            text = line.text
            if _blank(text):
                blank_seen = blank_seen or line
                self.i += 1
                continue
            m = _LIST.match(text)
            if m and not _HR.match(text):
                indent = _indent(m.group(1))
                while stack and indent < stack[-1]:
                    stack.pop()
                if not stack or indent > stack[-1]:
                    stack.append(indent)
                if blank_seen is not None:
                    self._mark_gap(blank_seen)
                blank_seen = None
                marker = m.group(2)
                rest = line.items(m.end())
                content_indent = indent + len(marker) + max(len(m.group(3)), 1)
                item = _RawBlock(
                    BlockKind.LIST_ITEM,
                    [_lstrip(rest)],
                    [],
                    line.term,
                    level=len(stack) - 1,
                    list_id=list_id,
                    ordered=marker[0].isdigit(),
                )
                self._emit(item)
                self.i += 1
                continue

            indent = _indent(text)
            if item is None:
                return
            if _FENCE.match(text) and indent > 0:
                if blank_seen is not None:
                    self._mark_gap(blank_seen)
                blank_seen = None
                code = self._fenced_code()
                code.list_id = list_id
                code.level = item.level
                self._emit(code)
                continue
            ends_list = blank_seen is not None and indent < min(content_indent, 2)
            if ends_list or (indent == 0 and self._starts_block(text)):
                if blank_seen is not None:
                    self._mark_gap(blank_seen)
                return
            if self.blocks[-1] is not item:  # text after a nested code block: new paragraph
                if blank_seen is not None:
                    self._mark_gap(blank_seen)
                blank_seen = None
                item = _RawBlock(
                    BlockKind.LIST_ITEM,
                    [_lstrip(line.items())],
                    [],
                    line.term,
                    level=item.level,
                    list_id=list_id,
                    ordered=item.ordered,
                )
                self._emit(item)
            elif blank_seen is not None:
                item.joins.append(("\n", *blank_seen.term))
                item.lines.append(_lstrip(line.items()))
                blank_seen = None
            else:
                _soft_break(item.lines[-1], item.last_term)
                item.lines[-1].extend(_lstrip(line.items()))
            item.last_term = line.term
            self.i += 1
        if blank_seen is not None:
            self._mark_gap(blank_seen)


def _lstrip(items: list[Item]) -> list[Item]:
    k = 0
    while k < len(items) and items[k][0] in " \t":
        k += 1
    return items[k:]


def _rstrip(items: list[Item]) -> None:
    while items and items[-1][0] in " \t":
        items.pop()


def _soft_break(items: list[Item], term: tuple[int, int]) -> None:
    """Join a wrapped line: trailing spaces and a hard-break backslash become one space."""
    _rstrip(items)
    if items and items[-1][0] == "\\" and (len(items) < 2 or items[-2][0] != "\\"):
        items.pop()
        _rstrip(items)
    if items:
        items.append((" ", *term))


# ---------------------------------------------------------------------------
# Inline markup

_ASCII_PUNCT = frozenset(string.punctuation)
_AUTOLINK = re.compile(r"<((?:https?|ftp|mailto):[^\s<>]*|[\w.+-]+@[\w-]+(?:\.[\w-]+)+)>")
_TAG = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)(?:\s[^<>]*)?/?>")
_ENTITY = re.compile(r"&(?:#[0-9]{1,7}|#[xX][0-9a-fA-F]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});")
# Formatting tags GitHub renders without showing; anything else is kept as literal text so
# payloads such as "<script>" quoted in prose stay visible as evidence.
_FORMAT_TAGS = frozenset(
    (
        "a abbr b bdi blockquote br center code del details div em h1 h2 h3 h4 h5 h6 hr i img "
        "ins kbd li mark ol p pre q s samp small span strike strong sub summary sup table tbody "
        "td tfoot th thead tr tt u ul"
    ).split()
)
_SPACE_TAGS = frozenset("br p div li tr td th h1 h2 h3 h4 h5 h6 hr".split())
# Python dunder names (``__init__``) are identifiers, not bold text, in advisory prose.
_DUNDER = re.compile(r"__[A-Za-z][A-Za-z0-9_]*?__(?![A-Za-z0-9_])")


@dataclass
class _Text:
    items: list[Item]


@dataclass
class _Code:
    items: list[Item]


@dataclass
class _Delim:
    char: str
    items: list[Item]
    can_open: bool
    can_close: bool


@dataclass
class _Link:
    children: list[_Node]


_Node = _Text | _Code | _Delim | _Link


def _tag_name(m: re.Match[str]) -> str:
    return m.group(1).lower()


def _is_space(ch: str) -> bool:
    return ch.isspace()


def _is_punct(ch: str) -> bool:
    return unicodedata.category(ch)[0] in "PS"


class _InlineParser:
    def __init__(self, items: list[Item]) -> None:
        self.items = items
        self.chars = "".join(ch for ch, _, _ in items)

    def parse(self, i: int, j: int) -> list[_Node]:
        nodes: list[_Node] = []
        buf: list[Item] = []
        items, chars = self.items, self.chars

        def flush() -> None:
            if buf:
                nodes.append(_Text(buf.copy()))
                buf.clear()

        k = i
        while k < j:
            ch = chars[k]
            if ch == "\\" and k + 1 < j and chars[k + 1] in _ASCII_PUNCT:
                buf.append((chars[k + 1], items[k][1], items[k + 1][2]))
                k += 2
            elif ch == "`":
                n = self._run(k, j, "`")
                close = self._closing_backticks(k + n, j, n)
                if close is None:
                    buf.extend(items[k : k + n])
                    k += n
                    continue
                flush()
                content = items[k + n : close]
                text = chars[k + n : close]
                if len(text) >= 2 and text[0] == " " and text[-1] == " " and text.strip():
                    content = content[1:-1]
                nodes.append(_Code(content))
                k = close + n
            elif ch == "<" and (m := _AUTOLINK.match(chars, k, j)):
                buf.extend(items[k + 1 : m.end() - 1])
                k = m.end()
            elif ch == "<" and chars.startswith("<!--", k) and (end := chars.find("-->", k, j)) > 0:
                k = end + 3
            elif ch == "<" and (m := _TAG.match(chars, k, j)) and _tag_name(m) in _FORMAT_TAGS:
                if _tag_name(m) in _SPACE_TAGS:
                    buf.append((" ", items[k][1], items[m.end() - 1][2]))
                k = m.end()
            elif ch == "&" and (m := _ENTITY.match(chars, k, j)):
                decoded = html.unescape(m.group())
                if decoded == m.group():
                    buf.extend(items[k : m.end()])
                else:
                    start, end = items[k][1], items[m.end() - 1][2]
                    buf.extend((c, start, end) for c in decoded)
                k = m.end()
            elif ch in "![" and (link := self._link(k, j)) is not None:
                flush()
                text_start, text_end, after = link
                nodes.append(_Link(self.parse(text_start, text_end)))
                k = after
            elif (
                ch == "_"
                and (k == i or not chars[k - 1].isalnum())
                and (m := _DUNDER.match(chars, k, j))
            ):
                buf.extend(items[k : m.end()])
                k = m.end()
            elif ch in "*_" or (ch == "~" and self._run(k, j, "~") == 2):
                n = self._run(k, j, ch)
                flush()
                nodes.append(self._delim(k, n, i, j))
                k += n
            else:
                buf.append(items[k])
                k += 1
        flush()
        return nodes

    def _run(self, k: int, j: int, ch: str) -> int:
        n = 0
        while k + n < j and self.chars[k + n] == ch:
            n += 1
        return n

    def _closing_backticks(self, k: int, j: int, n: int) -> int | None:
        while k < j:
            if self.chars[k] == "`":
                m = self._run(k, j, "`")
                if m == n:
                    return k
                k += m
            else:
                k += 1
        return None

    def _delim(self, k: int, n: int, i: int, j: int) -> _Delim:
        ch = self.chars[k]
        before = self.chars[k - 1] if k > i else " "
        after = self.chars[k + n] if k + n < j else " "
        left = not _is_space(after) and (
            not _is_punct(after) or _is_space(before) or _is_punct(before)
        )
        right = not _is_space(before) and (
            not _is_punct(before) or _is_space(after) or _is_punct(after)
        )
        if ch == "_":
            can_open = left and (not right or _is_punct(before))
            can_close = right and (not left or _is_punct(after))
        else:
            can_open, can_close = left, right
        return _Delim(ch, list(self.items[k : k + n]), can_open, can_close)

    def _link(self, k: int, j: int) -> tuple[int, int, int] | None:
        """Return (text_start, text_end, index_after) for an inline link or image.

        Reference-style links are left literal: without their definitions they are
        indistinguishable from prose such as ``list[str][0]``.
        """
        start = k + 1 if self.chars[k] == "!" else k
        if start >= j or self.chars[start] != "[":
            return None
        close = self._match_bracket(start, j)
        if close is None or close + 1 >= j or self.chars[close + 1] != "(":
            return None
        end = self._match_paren(close + 1, j)
        if end is None:
            return None
        return start + 1, close, end + 1

    def _match_bracket(self, k: int, j: int) -> int | None:
        depth = 0
        m = k
        while m < j:
            ch = self.chars[m]
            if ch == "\\":
                m += 2
                continue
            if ch == "`":
                n = self._run(m, j, "`")
                close = self._closing_backticks(m + n, j, n)
                m = (close + n) if close is not None else m + n
                continue
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return m
            m += 1
        return None

    def _match_paren(self, k: int, j: int) -> int | None:
        depth = 0
        for m in range(k, j):
            ch = self.chars[m]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return m
        return None


def _resolve_emphasis(nodes: list[_Node]) -> None:
    """Simplified CommonMark delimiter matching; unmatched delimiters stay literal."""
    for node in nodes:
        if isinstance(node, _Link):
            _resolve_emphasis(node.children)
    for ci, closer in enumerate(nodes):
        if not isinstance(closer, _Delim) or not closer.can_close:
            continue
        while closer.items:
            opener_index = None
            for oi in range(ci - 1, -1, -1):
                opener = nodes[oi]
                if (
                    isinstance(opener, _Delim)
                    and opener.char == closer.char
                    and opener.can_open
                    and opener.items
                    and not _rule_of_three(opener, closer)
                ):
                    opener_index = oi
                    break
            if opener_index is None:
                break
            opener = nodes[opener_index]
            assert isinstance(opener, _Delim)
            use = 2 if len(opener.items) >= 2 and len(closer.items) >= 2 else 1
            del opener.items[len(opener.items) - use :]
            del closer.items[:use]
            for between in nodes[opener_index + 1 : ci]:
                if isinstance(between, _Delim):
                    between.can_open = between.can_close = False


def _rule_of_three(opener: _Delim, closer: _Delim) -> bool:
    if opener.char == "~":
        return False
    both = opener.can_close or closer.can_open
    total = len(opener.items) + len(closer.items)
    return both and total % 3 == 0 and not (len(opener.items) % 3 == 0 == len(closer.items) % 3)


def _nfc(items: list[Item]) -> list[Item]:
    """NFC-normalise prose cluster by cluster so every output character keeps its raw range."""
    out: list[Item] = []
    cluster: list[Item] = []

    def flush() -> None:
        if not cluster:
            return
        text = "".join(ch for ch, _, _ in cluster)
        normal = unicodedata.normalize("NFC", text)
        if normal == text:
            out.extend(cluster)
        else:
            out.extend((ch, cluster[0][1], cluster[-1][2]) for ch in normal)
        cluster.clear()

    for item in items:
        ch = item[0]
        if cluster and (unicodedata.combining(ch) or 0x1160 <= ord(ch) <= 0x11FF):
            cluster.append(item)
        else:
            flush()
            cluster.append(item)
    flush()
    return out


def _flatten(nodes: list[_Node], out: list[Item], code: list[tuple[int, int]]) -> None:
    prose: list[Item] = []

    def flush() -> None:
        out.extend(_nfc(prose))
        prose.clear()

    for node in nodes:
        if isinstance(node, _Text | _Delim):
            prose.extend(node.items)
        elif isinstance(node, _Code):
            flush()
            if node.items:
                code.append((len(out), len(out) + len(node.items)))
                out.extend(node.items)
        else:
            flush()
            _flatten(node.children, out, code)
    flush()


def render_inline(items: list[Item]) -> tuple[list[Item], list[tuple[int, int]]]:
    """Strip inline markup from one logical line; returns items and code ranges within them."""
    parser = _InlineParser(items)
    nodes = parser.parse(0, len(items))
    _resolve_emphasis(nodes)
    out: list[Item] = []
    code: list[tuple[int, int]] = []
    _flatten(nodes, out, code)
    # Trim surrounding whitespace, shifting code ranges to match.
    lead = 0
    while lead < len(out) and out[lead][0].isspace() and not _starts_code(code, lead):
        lead += 1
    trail = len(out)
    while trail > lead and out[trail - 1][0].isspace() and not _ends_code(code, trail):
        trail -= 1
    trimmed = out[lead:trail]
    ranges = [(s - lead, e - lead) for s, e in code if s >= lead and e <= trail]
    return trimmed, ranges


def _starts_code(code: list[tuple[int, int]], index: int) -> bool:
    return any(s <= index < e for s, e in code)


def _ends_code(code: list[tuple[int, int]], end: int) -> bool:
    return any(s < end <= e for s, e in code)


# ---------------------------------------------------------------------------
# Assembly


def canonicalize(raw: str) -> CanonicalText:
    """Convert raw advisory Markdown into canonical text with an offset map."""
    raw_blocks = _Parser(_split_lines(raw)).run()
    out: list[Item] = []
    blocks: list[Block] = []
    code_spans: list[tuple[int, int]] = []
    prev_term: tuple[int, int] | None = None

    for raw_block in raw_blocks:
        rendered: list[list[Item]] = []
        line_code: list[list[tuple[int, int]]] = []
        joins: list[Item] = []
        for index, line in enumerate(raw_block.lines):
            ranges: list[tuple[int, int]] = []
            if raw_block.verbatim:
                items = line
            else:
                items, ranges = render_inline(line)
                if not items:
                    continue
            if rendered:
                joins.append(raw_block.joins[index - 1])
            rendered.append(items)
            line_code.append(ranges)
        if not any(rendered):
            continue

        if prev_term is not None:
            out.append(("\n", *prev_term))
            if raw_block.gap is not None:
                out.append(("\n", *raw_block.gap))
        start = len(out)
        for index, items in enumerate(rendered):
            if index:
                out.append(joins[index - 1])
            base = len(out)
            code_spans.extend((base + s, base + e) for s, e in line_code[index])
            out.extend(items)
        end = len(out)
        if raw_block.verbatim:
            code_spans.append((start, end))
        blocks.append(
            Block(
                raw_block.kind,
                start,
                end,
                raw_block.level,
                raw_block.list_id,
                raw_block.ordered,
            )
        )
        prev_term = raw_block.last_term

    return CanonicalText(
        raw=raw,
        text="".join(ch for ch, _, _ in out),
        raw_starts=tuple(s for _, s, _ in out),
        raw_ends=tuple(e for _, _, e in out),
        blocks=tuple(blocks),
        code_spans=tuple(sorted(code_spans)),
    )
