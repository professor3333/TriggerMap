"""SQLite storage for the review application (WAL mode).

Tables:
- advisories / advisory_aliases: the served advisory snapshot (refreshed by a job);
- predictions: cache keyed by content hash, model, preprocessing and review-policy versions;
- users: API tokens (only SHA-256 hashes of random tokens are stored);
- reviews + review_events: a review is a sequence of full states. Events are append-only,
  enforced by triggers, so the correction history cannot be rewritten.

Reviewer answers live only in reviews/review_events, never in the shared prediction cache.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import uuid
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS advisories (
    advisory_id TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    title TEXT NOT NULL,
    packages TEXT NOT NULL,
    published TEXT,
    source_commit TEXT,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS advisory_aliases (
    alias TEXT NOT NULL,
    advisory_id TEXT NOT NULL REFERENCES advisories(advisory_id) ON DELETE CASCADE,
    PRIMARY KEY (alias, advisory_id)
);
CREATE TABLE IF NOT EXISTS predictions (
    cache_key TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL,
    model_id TEXT NOT NULL,
    preprocessing_version TEXT NOT NULL,
    review_policy_version TEXT NOT NULL,
    extraction_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    token_hash TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    idempotency_key TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    advisory_id TEXT,
    title TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    model_id TEXT NOT NULL,
    preprocessing_version TEXT NOT NULL,
    review_policy_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (user_id, idempotency_key)
);
CREATE TABLE IF NOT EXISTS review_events (
    review_id TEXT NOT NULL REFERENCES reviews(id),
    seq INTEGER NOT NULL,
    idempotency_key TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    kind TEXT NOT NULL,
    state_json TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL,
    PRIMARY KEY (review_id, seq),
    UNIQUE (review_id, idempotency_key)
);
CREATE TRIGGER IF NOT EXISTS review_events_no_update BEFORE UPDATE ON review_events
BEGIN SELECT RAISE(ABORT, 'review_events is append-only'); END;
CREATE TRIGGER IF NOT EXISTS review_events_no_delete BEFORE DELETE ON review_events
BEGIN SELECT RAISE(ABORT, 'review_events is append-only'); END;
"""


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def request_hash(payload: Any) -> str:
    return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False))


class IdempotencyConflict(Exception):
    """The idempotency key was already used with a different request."""


@dataclass(frozen=True)
class User:
    id: int
    name: str


@dataclass(frozen=True)
class AdvisoryRecord:
    advisory_id: str
    content_hash: str
    raw_text: str
    title: str
    packages: tuple[str, ...]
    published: str | None
    source_commit: str | None


class Store:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript(SCHEMA)
            db.execute(
                "INSERT OR IGNORE INTO meta(key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA busy_timeout=5000")
            yield db
        finally:
            db.close()

    def set_meta(self, key: str, value: str) -> None:
        with self.connect() as db:
            db.execute("INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)", (key, value))

    def get_meta(self, key: str) -> str | None:
        with self.connect() as db:
            row = db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return None if row is None else str(row[0])

    def journal_mode(self) -> str:
        with self.connect() as db:
            return str(db.execute("PRAGMA journal_mode").fetchone()[0])

    def ping(self) -> bool:
        with self.connect() as db:
            row = db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
        return row is not None and str(row[0]) == str(SCHEMA_VERSION)

    # -- advisories

    def upsert_advisories(self, records: Sequence[tuple[AdvisoryRecord, Sequence[str]]]) -> int:
        stamp = now()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            for record, aliases in records:
                db.execute(
                    """INSERT INTO advisories VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(advisory_id) DO UPDATE SET content_hash=excluded.content_hash,
                       raw_text=excluded.raw_text, title=excluded.title,
                       packages=excluded.packages, published=excluded.published,
                       source_commit=excluded.source_commit, updated_at=excluded.updated_at""",
                    (
                        record.advisory_id,
                        record.content_hash,
                        record.raw_text,
                        record.title,
                        json.dumps(list(record.packages)),
                        record.published,
                        record.source_commit,
                        stamp,
                    ),
                )
                db.execute(
                    "DELETE FROM advisory_aliases WHERE advisory_id=?", (record.advisory_id,)
                )
                db.executemany(
                    "INSERT OR IGNORE INTO advisory_aliases VALUES (?, ?)",
                    [(alias, record.advisory_id) for alias in {record.advisory_id, *aliases}],
                )
            db.execute("COMMIT")
        return len(records)

    def advisory(self, identifier: str) -> AdvisoryRecord | None:
        """Look up by GHSA id or by any alias (CVE, PYSEC)."""
        with self.connect() as db:
            row = db.execute(
                """SELECT a.* FROM advisories a JOIN advisory_aliases x
                   ON x.advisory_id = a.advisory_id WHERE x.alias = ? ORDER BY a.advisory_id
                   LIMIT 1""",
                (identifier,),
            ).fetchone()
        if row is None:
            return None
        return AdvisoryRecord(
            row["advisory_id"],
            row["content_hash"],
            row["raw_text"],
            row["title"],
            tuple(json.loads(row["packages"])),
            row["published"],
            row["source_commit"],
        )

    def advisory_count(self) -> int:
        with self.connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM advisories").fetchone()[0])

    # -- prediction cache (no reviewer data)

    @staticmethod
    def cache_key(content_hash: str, model_id: str, preprocessing: str, policy: str) -> str:
        return sha256(f"{content_hash}|{model_id}|{preprocessing}|{policy}")

    def cached_prediction(self, key: str) -> str | None:
        with self.connect() as db:
            row = db.execute(
                "SELECT extraction_json FROM predictions WHERE cache_key=?", (key,)
            ).fetchone()
        return None if row is None else str(row[0])

    def store_prediction(
        self, key: str, content_hash: str, model_id: str, preprocessing: str, policy: str, data: str
    ) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO predictions VALUES (?, ?, ?, ?, ?, ?, ?)",
                (key, content_hash, model_id, preprocessing, policy, data, now()),
            )

    # -- users

    def create_user(self, name: str) -> str:
        """Create a user and return a new API token (shown once, stored only as a hash)."""
        token = "tm_" + secrets.token_urlsafe(32)
        with self.connect() as db:
            db.execute(
                "INSERT INTO users(name, token_hash, created_at) VALUES (?, ?, ?)",
                (name, sha256(token), now()),
            )
        return token

    def user_for_token(self, token: str) -> User | None:
        with self.connect() as db:
            row = db.execute(
                "SELECT id, name FROM users WHERE token_hash=?", (sha256(token),)
            ).fetchone()
        return None if row is None else User(int(row["id"]), str(row["name"]))

    # -- reviews

    def create_review(
        self,
        user: User,
        idempotency_key: str,
        payload: dict[str, Any],
        meta: dict[str, Any],
        state: dict[str, Any],
    ) -> tuple[str, bool]:
        """Create a review with its first state; returns (review id, created?)."""
        digest = request_hash(payload)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id, request_hash FROM reviews WHERE user_id=? AND idempotency_key=?",
                (user.id, idempotency_key),
            ).fetchone()
            if row is not None:
                db.execute("ROLLBACK")
                if row["request_hash"] != digest:
                    raise IdempotencyConflict(idempotency_key)
                return str(row["id"]), False
            review_id = str(uuid.uuid4())
            stamp = now()
            db.execute(
                "INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    review_id,
                    user.id,
                    idempotency_key,
                    digest,
                    meta.get("advisory_id"),
                    meta["title"],
                    meta["raw_text"],
                    meta["content_hash"],
                    meta["model_id"],
                    meta["preprocessing_version"],
                    meta["review_policy_version"],
                    stamp,
                ),
            )
            db.execute(
                "INSERT INTO review_events VALUES (?, 1, ?, ?, 'created', ?, NULL, ?)",
                (review_id, idempotency_key, digest, json.dumps(state, sort_keys=True), stamp),
            )
            db.execute("COMMIT")
        return review_id, True

    def append_revision(
        self,
        review_id: str,
        idempotency_key: str,
        payload: dict[str, Any],
        state: dict[str, Any],
        note: str | None,
    ) -> tuple[int, bool]:
        """Append a new state; returns (sequence number, created?)."""
        digest = request_hash(payload)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT seq, request_hash FROM review_events "
                "WHERE review_id=? AND idempotency_key=?",
                (review_id, idempotency_key),
            ).fetchone()
            if row is not None:
                db.execute("ROLLBACK")
                if row["request_hash"] != digest:
                    raise IdempotencyConflict(idempotency_key)
                return int(row["seq"]), False
            seq = int(
                db.execute(
                    "SELECT COALESCE(MAX(seq), 0) + 1 FROM review_events WHERE review_id=?",
                    (review_id,),
                ).fetchone()[0]
            )
            db.execute(
                "INSERT INTO review_events VALUES (?, ?, ?, ?, 'revised', ?, ?, ?)",
                (
                    review_id,
                    seq,
                    idempotency_key,
                    digest,
                    json.dumps(state, sort_keys=True),
                    note,
                    now(),
                ),
            )
            db.execute("COMMIT")
        return seq, True

    def review(self, review_id: str, user: User) -> dict[str, Any] | None:
        """The review header, its current state and its full event history (owner only)."""
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM reviews WHERE id=? AND user_id=?", (review_id, user.id)
            ).fetchone()
            if row is None:
                return None
            events = db.execute(
                "SELECT seq, kind, state_json, note, created_at FROM review_events "
                "WHERE review_id=? ORDER BY seq",
                (review_id,),
            ).fetchall()
        # dict(row): iterating a sqlite3.Row yields values, not column names.
        header = {k: v for k, v in dict(row).items() if k not in ("user_id", "request_hash")}
        history = [
            {"seq": e["seq"], "kind": e["kind"], "note": e["note"], "created_at": e["created_at"]}
            for e in events
        ]
        return {
            **header,
            "state": json.loads(events[-1]["state_json"]),
            "states": [json.loads(e["state_json"]) for e in events],
            "history": history,
        }

    def reviews(self, user: User) -> list[dict[str, Any]]:
        with self.connect() as db:
            rows = db.execute(
                """SELECT r.id, r.advisory_id, r.title, r.created_at,
                   (SELECT MAX(created_at) FROM review_events e WHERE e.review_id = r.id)
                   AS updated_at FROM reviews r WHERE r.user_id=? ORDER BY updated_at DESC""",
                (user.id,),
            ).fetchall()
        return [dict(row) for row in rows]
