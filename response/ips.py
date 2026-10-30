"""In-memory IPS response simulator (does not change host firewall rules)."""

from red_team.safety import require_lab_target

blocked_ips: set[str] = set()


def check_and_block(ip: str, severity: str) -> bool:
    """Record a simulated block decision for high-severity private lab IPs."""
    target = require_lab_target(ip)
    if str(severity).upper() in {"HIGH", "CRITICAL"}:
        blocked_ips.add(target)
        print(f"[IPS SIMULATION] Would block lab source: {target}")
        return True
    return False


def is_blocked(ip: str) -> bool:
    try:
        target = require_lab_target(ip)
    except ValueError:
        return False
    return target in blocked_ips
