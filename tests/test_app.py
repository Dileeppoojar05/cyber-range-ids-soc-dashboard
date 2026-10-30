import os
import tempfile
import unittest
from pathlib import Path

_TEST_DIRECTORY = tempfile.TemporaryDirectory()
os.environ["CYBER_RANGE_DB_PATH"] = str(Path(_TEST_DIRECTORY.name) / "dashboard-test.sqlite3")

from dashboard.app import app  # noqa: E402


class DashboardSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"SOC Console", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_public_target_is_rejected_before_launch(self):
        response = self.client.post(
            "/attack",
            data={"target": "8.8.8.8", "attack_type": "scan"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"private or loopback IPv4", response.data)


if __name__ == "__main__":
    unittest.main()
