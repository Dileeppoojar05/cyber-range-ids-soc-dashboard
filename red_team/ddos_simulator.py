import sys
import time

def ddos(target):
    print(f"[DDOS] Simulating traffic flood on {target}")

    for i in range(10):
        print(f"Packet {i} sent")
        time.sleep(0.2)

    print("[DONE] DDOS simulation complete")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target: ")
    ddos(target)
