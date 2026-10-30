import os
import tempfile
import unittest
from pathlib import Path

from database.db import fetch_alert_stats, fetch_alerts, init_db, insert_alert
from detection.engine import classify_attack
from red_team.safety import is_allowed_lab_target


class TargetScopeTests(unittest.TestCase):
    def test_loopback_and_private_addresses_are_allowed(self):
        self.assertTrue(is_allowed_lab_target("127.0.0.1"))
        self.assertTrue(is_allowed_lab_target("192.168.1.10"))
        self.assertTrue(is_allowed_lab_target("10.0.0.5"))

    def test_public_and_non_ip_targets_are_rejected(self):
        self.assertFalse(is_allowed_lab_target("8.8.8.8"))
        self.assertFalse(is_allowed_lab_target("example.com"))
        self.assertFalse(is_allowed_lab_target("0.0.0.0"))


class DetectionTests(unittest.TestCase):
    def test_signatures_are_classified_case_insensitively(self):
        self.assertEqual(classify_attack("ET SCAN Portscan"), ("Port Scan", "MEDIUM"))
        self.assertEqual(classify_attack("DDoS flood"), ("DDoS Attack", "HIGH"))
        self.assertEqual(classify_attack("unknown event"), ("Unknown", "LOW"))


class DatabaseTests(unittest.TestCase):
    def test_alert_insert_deduplication_and_stats(self):
        previous = os.environ.get("CYBER_RANGE_DB_PATH")
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["CYBER_RANGE_DB_PATH"] = str(Path(temp_dir) / "test.sqlite3")
            try:
                init_db()
                self.assertTrue(
                    insert_alert(
                        "127.0.0.1",
                        "Port Scan",
                        "MEDIUM",
                        event_id="test-event-1",
                        source="suricata",
                    )
                )
                self.assertFalse(
                    insert_alert(
                        "127.0.0.1",
                        "Port Scan",
                        "MEDIUM",
                        event_id="test-event-1",
                        source="suricata",
                    )
                )
                self.assertEqual(len(fetch_alerts()), 1)
                self.assertEqual(fetch_alert_stats()["medium"], 1)
            finally:
                if previous is None:
                    os.environ.pop("CYBER_RANGE_DB_PATH", None)
                else:
                    os.environ["CYBER_RANGE_DB_PATH"] = previous


if __name__ == "__main__":
    unittest.main()
