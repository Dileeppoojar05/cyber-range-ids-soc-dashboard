"""Offline DDoS traffic-pattern demonstration; sends no network packets."""

import sys
import time

from safety import require_lab_target


def ddos(target: str) -> None:
    target = require_lab_target(target)
    print(f"[DDoS SIMULATION] Lab target: {target}")
    for index in range(1, 11):
        print(f"Simulated traffic event {index}/10")
        time.sleep(0.1)
    print("[DONE] No packets were sent; traffic was simulated locally.")


if __name__ == "__main__":
    try:
        ddos(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    except ValueError as error:
        print(f"[BLOCKED] {error}", file=sys.stderr)
        raise SystemExit(2)
