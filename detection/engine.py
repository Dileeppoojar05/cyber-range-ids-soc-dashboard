def classify_attack(signature):
    sig = signature.lower()

    if "ddos" in sig or "flood" in sig:
        return "DDoS Attack", "HIGH"

    elif "scan" in sig:
        return "Port Scan", "MEDIUM"

    elif "brute" in sig:
        return "Brute Force", "HIGH"

    elif "web" in sig:
        return "Web Attack", "MEDIUM"

    else:
        return "Unknown", "LOW"
