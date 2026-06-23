import sys
import time
import json

LOG_FILE = "eve.json"

def write_event(target, i):
    event = {
        "event_type": "alert",
        "timestamp": time.time(),
        "src_ip": target,
        "alert": {
            "signature": "DDoS flood"
        }
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

def ddos(target):
    print(f"[DDOS] Simulating traffic flood on {target}")

    for i in range(10):
        print(f"Packet {i} sent")
        write_event(target, i)
        time.sleep(0.2)

    print("[DONE] DDOS simulation complete")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Target: ")
    ddos(target)
