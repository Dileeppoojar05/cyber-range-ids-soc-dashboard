"""Offline web-attack concept demo; does not send HTTP requests or payloads."""

import sys
import time

from safety import require_lab_target


def simulate_web_attack(target: str) -> None:
    target = require_lab_target(target)
    print(f"[WEB ATTACK SIMULATION] Lab target: {target}")
    for scenario in ("SQL injection indicator", "XSS indicator", "Path traversal indicator"):
        print(f"Demonstrating detection scenario: {scenario}")
        time.sleep(0.15)
    print("[DONE] No HTTP requests or exploit payloads were sent.")


if __name__ == "__main__":
    try:
        simulate_web_attack(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    except ValueError as error:
        print(f"[BLOCKED] {error}", file=sys.stderr)
        raise SystemExit(2)
