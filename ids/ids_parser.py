import json
from detection.engine import classify_attack 
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "eve.json")   # path from dashboard

def parse_logs(insert_alert_func):
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                data = json.loads(line)

                if data.get("event_type") == "alert":
                    timestamp = data.get("timestamp")
                    src_ip = data.get("src_ip")

                    alert = data.get("alert", {})
                    signature = alert.get("signature", "Unknown")

                    attack_type, severity = classify_attack(signature)

                    insert_alert_func(src_ip, attack_type, severity)

    except FileNotFoundError:
        print("[IDS] eve.json not found")
if __name__ == "__main__":
    def insert_alert(src_ip, attack_type, severity):
        print(f"[ALERT] {src_ip} | {attack_type} | {severity}")

    parse_logs(insert_alert)
