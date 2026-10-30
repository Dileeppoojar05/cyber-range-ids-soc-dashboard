"""Generate sample DoS EVE-style records without sending network traffic."""

import json
import sys
import time
from pathlib import Path

from safety import require_lab_target

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "instance" / "simulated-eve.jsonl"


def write_event(target: str, index: int) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event_type": "alert",
        "timestamp": time.time(),
        "src_ip": target,
        "alert": {"signature": "DoS flood simulation"},
        "simulation_id": index,
    }
    with OUTPUT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def ddos(target: str) -> None:
    target = require_lab_target(target)
    print(f"[DoS SIMULATION] Lab target: {target}")
    for index in range(1, 11):
        write_event(target, index)
        print(f"Recorded simulated event {index}/10")
        time.sleep(0.1)
    print(f"[DONE] Sample events written to {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    try:
        ddos(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    except ValueError as error:
        print(f"[BLOCKED] {error}", file=sys.stderr)
        raise SystemExit(2)
