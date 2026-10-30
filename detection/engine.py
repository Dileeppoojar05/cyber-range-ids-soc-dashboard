"""Small signature classifier for the educational Cyber Range."""


def classify_attack(signature: str) -> tuple[str, str]:
    """Map an IDS signature to a display category and severity."""
    sig = str(signature or "").casefold()

    if any(term in sig for term in ("ddos", "dos flood", "flood", "udp flood")):
        return "DDoS Attack", "HIGH"
    if any(term in sig for term in ("brute", "password attack", "login attempt")):
        return "Brute Force", "HIGH"
    if any(term in sig for term in ("sql injection", "xss", "web attack", "web application")):
        return "Web Attack", "MEDIUM"
    if any(term in sig for term in ("scan", "portscan", "recon")):
        return "Port Scan", "MEDIUM"
    return "Unknown", "LOW"
