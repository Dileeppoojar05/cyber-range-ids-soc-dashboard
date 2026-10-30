"""Import Suricata EVE JSON alert events into the Cyber Range database."""

import hashlib
import json
from pathlib import Path
from typing import Callable, Any

from detection.engine import classify_attack

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = PROJECT_ROOT / "eve.json"


def parse_logs(
    insert_alert_func: Callable[..., Any], log_file: str | Path = LOG_FILE
) -> int:
    """Import valid alert lines and return the number of newly inserted records.

    A SHA-256 fingerprint of each original line is used as an idempotency key.
    Re-importing the same EVE file therefore does not duplicate existing alerts.
    """
    path = Path(log_file)
    inserted = 0
    try:
        with path.open("r", encoding="utf-8") as log_handle:
            for line in log_handle:
                raw_line = line.strip()
                if not raw_line:
                    continue
                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                if not isinstance(event, dict) or event.get("event_type") != "alert":
                    continue

                alert = event.get("alert") or {}
                if not isinstance(alert, dict):
                    alert = {}
                signature = str(alert.get("signature") or "Unknown")
                attack_type, severity = classify_attack(signature)
                event_fingerprint = hashlib.sha256(raw_line.encode("utf-8")).hexdigest()

                was_inserted = insert_alert_func(
                    str(event.get("src_ip") or "unknown"),
                    attack_type,
                    severity,
                    timestamp=event.get("timestamp"),
                    event_id=event_fingerprint,
                    source="suricata",
                    details=signature,
                )
                if was_inserted:
                    inserted += 1
    except FileNotFoundError:
        print(f"[IDS] EVE log not found: {path}")
    except OSError as error:
        print(f"[IDS] Could not read EVE log: {error}")

    return inserted


if __name__ == "__main__":
    from database.db import init_db, insert_alert

    init_db()
    print(f"[IDS] Imported {parse_logs(insert_alert)} new alert(s).")
