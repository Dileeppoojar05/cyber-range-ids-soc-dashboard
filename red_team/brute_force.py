"""Offline brute-force concept simulation; performs no authentication attempts."""

import sys
import time

from safety import require_lab_target


def brute_force(target: str) -> None:
    target = require_lab_target(target)
    print(f"[BRUTE-FORCE SIMULATION] Lab target: {target}")
    sample_attempts = ("candidate-01", "candidate-02", "candidate-03", "candidate-04")
    for number, _ in enumerate(sample_attempts, start=1):
        print(f"Simulated authentication attempt {number}: rejected (offline demo)")
        time.sleep(0.1)
    print("[DONE] No login service was contacted; simulation only.")


if __name__ == "__main__":
    try:
        brute_force(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    except ValueError as error:
        print(f"[BLOCKED] {error}", file=sys.stderr)
        raise SystemExit(2)
