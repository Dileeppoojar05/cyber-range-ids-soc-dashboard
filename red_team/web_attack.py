import sys
import time

def simulate_web_attack(target):
    print(f"[WEB ATTACK] Target: {target}")

    attacks = [
        "SQL Injection",
        "XSS",
        "Directory Traversal"
    ]

    for attack in attacks:
        print(f"Simulating {attack}...")
        time.sleep(1)

    print("[DONE] Web attack simulation finished")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target URL: ")
    simulate_web_attack(target)
