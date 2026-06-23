import sys
import time

def brute_force(target):
    print(f"[BRUTE] Simulating brute force on {target}")

    passwords = ["admin", "123456", "password", "root"]

    for pwd in passwords:
        print(f"Trying: {pwd}")
        time.sleep(0.5)

    print("[RESULT] Simulation complete")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target: ")
    brute_force(target)
