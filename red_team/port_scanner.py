"""Small TCP connectivity check restricted to private IPv4 lab addresses."""

import socket
import sys

from safety import require_lab_target

PORTS = (21, 22, 23, 80, 443)


def scan(target: str) -> list[int]:
    target = require_lab_target(target)
    print(f"[SCAN SIMULATION] Target: {target}; ports: {', '.join(map(str, PORTS))}")
    open_ports: list[int] = []
    for port in PORTS:
        try:
            with socket.create_connection((target, port), timeout=0.4):
                open_ports.append(port)
                print(f"[OPEN] TCP/{port}")
        except (TimeoutError, OSError):
            print(f"[CLOSED/FILTERED] TCP/{port}")
    return open_ports


if __name__ == "__main__":
    try:
        scan(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    except ValueError as error:
        print(f"[BLOCKED] {error}", file=sys.stderr)
        raise SystemExit(2)
