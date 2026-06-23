blocked_ips = set()

def check_and_block(ip, severity):
    if severity == "HIGH":
        blocked_ips.add(ip)
        print(f"[IPS] Blocked IP: {ip}")

def is_blocked(ip):
    return ip in blocked_ips
