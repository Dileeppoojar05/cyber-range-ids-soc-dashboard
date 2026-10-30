"""SQLite persistence for Cyber Range alerts."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_db_path() -> Path:
    """Return the configured database path, defaulting to an ignored instance file."""
    configured = os.environ.get("CYBER_RANGE_DB_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return PROJECT_ROOT / "instance" / "cyber_range.sqlite3"


def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path), timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def _normalise_timestamp(value: Any) -> str:
    if value is None or value == "":
        return datetime.now(timezone.utc).isoformat(timespec="seconds")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat(timespec="seconds")
    return str(value)


def init_db() -> None:
    """Create the alert table and indexes when the application starts."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                attack_type TEXT NOT NULL,
                severity TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
                source TEXT NOT NULL DEFAULT 'simulation',
                details TEXT,
                event_id TEXT UNIQUE
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp DESC)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity)"
        )


def insert_alert(
    source_ip: str,
    attack_type: str,
    severity: str,
    *,
    timestamp: Any = None,
    event_id: str | None = None,
    source: str = "simulation",
    details: str | None = None,
) -> bool:
    """Insert an alert; event_id makes repeated IDS log imports idempotent."""
    severity_value = str(severity).upper()
    if severity_value not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError(f"Unsupported alert severity: {severity}")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO alerts
                (timestamp, source_ip, attack_type, severity, source, details, event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _normalise_timestamp(timestamp),
                str(source_ip),
                str(attack_type),
                severity_value,
                str(source),
                str(details)[:1000] if details else None,
                event_id,
            ),
        )
        return cursor.rowcount == 1


def fetch_alerts(limit: int = 100) -> list[dict[str, Any]]:
    safe_limit = max(1, min(int(limit), 500))
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, timestamp, source_ip, attack_type, severity, source, details
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def fetch_alert_stats() -> dict[str, int]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical,
                SUM(CASE WHEN severity = 'HIGH' THEN 1 ELSE 0 END) AS high,
                SUM(CASE WHEN severity = 'MEDIUM' THEN 1 ELSE 0 END) AS medium,
                SUM(CASE WHEN severity = 'LOW' THEN 1 ELSE 0 END) AS low
            FROM alerts
            """
        ).fetchone()
    return {key: int(row[key] or 0) for key in ("total", "critical", "high", "medium", "low")}
