import json
import tempfile
import unittest
from pathlib import Path

from ids.ids_parser import parse_logs


class EVEParserTests(unittest.TestCase):
    def test_alert_events_are_classified_and_repeat_imports_are_idempotent(self):
        events = [
            {
                "event_type": "alert",
                "timestamp": "2026-10-30T12:00:00.000000+0000",
                "src_ip": "192.168.56.10",
                "alert": {"signature": "ET SCAN Portscan"},
            },
            {"event_type": "stats", "src_ip": "192.168.56.10"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eve.json"
            path.write_text(
                "\n".join([json.dumps(events[0]), "{broken-json", json.dumps(events[1])]) + "\n",
                encoding="utf-8",
            )
            inserted_ids = set()
            captured = []

            def insert_once(source_ip, attack_type, severity, **kwargs):
                event_id = kwargs.get("event_id")
                if event_id in inserted_ids:
                    return False
                inserted_ids.add(event_id)
                captured.append((source_ip, attack_type, severity, kwargs))
                return True

            self.assertEqual(parse_logs(insert_once, path), 1)
            self.assertEqual(parse_logs(insert_once, path), 0)
            self.assertEqual(len(captured), 1)
            self.assertEqual(captured[0][1:3], ("Port Scan", "MEDIUM"))
            self.assertEqual(captured[0][3]["source"], "suricata")


if __name__ == "__main__":
    unittest.main()
