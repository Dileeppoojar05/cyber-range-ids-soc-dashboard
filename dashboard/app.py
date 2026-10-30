"""Local-only Flask dashboard for the Cyber Range project."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from flask import Flask, flash, redirect, render_template, request, url_for

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db import fetch_alert_stats, fetch_alerts, init_db, insert_alert
from ids.ids_parser import parse_logs
from red_team.safety import require_lab_target
from response.ips import check_and_block

app = Flask(__name__)
app.secret_key = os.environ.get("CYBER_RANGE_SECRET_KEY") or os.urandom(32)
init_db()

SIMULATIONS = {
    "scan": ("Port Scan", "MEDIUM", PROJECT_ROOT / "red_team" / "port_scanner.py"),
    "brute": ("Brute Force Simulation", "HIGH", PROJECT_ROOT / "red_team" / "brute_force.py"),
    "web": ("Web Attack Simulation", "MEDIUM", PROJECT_ROOT / "red_team" / "web_attack.py"),
    "ddos": ("DDoS Traffic Simulation", "HIGH", PROJECT_ROOT / "red_team" / "ddos_simulator.py"),
}


@app.get("/")
def index():
    alerts = fetch_alerts(limit=500)
    severity_filter = request.args.get("severity", "ALL").upper()
    query = request.args.get("q", "").strip().lower()

    if severity_filter in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        alerts = [item for item in alerts if item["severity"] == severity_filter]
    else:
        severity_filter = "ALL"

    if query:
        alerts = [
            item for item in alerts
            if query in item["source_ip"].lower()
            or query in item["attack_type"].lower()
            or query in (item["details"] or "").lower()
        ]

    return render_template(
        "index.html",
        alerts=alerts,
        stats=fetch_alert_stats(),
        severity_filter=severity_filter,
        query=request.args.get("q", ""),
    )


@app.post("/attack")
def attack():
    try:
        target = require_lab_target(request.form.get("target", ""))
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    attack_key = request.form.get("attack_type", "")
    simulation = SIMULATIONS.get(attack_key)
    if simulation is None:
        flash("Choose a valid simulation scenario.", "error")
        return redirect(url_for("index"))

    attack_name, severity, script = simulation
    try:
        completed = subprocess.run(
            [sys.executable, str(script), target],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        flash("Simulation stopped because it exceeded the 15-second limit.", "error")
        return redirect(url_for("index"))

    output = (completed.stdout or "")[-1200:]
    if completed.returncode != 0:
        message = (completed.stderr or output or "Simulation failed.")[-500:]
        flash(f"Simulation failed: {message}", "error")
        return redirect(url_for("index"))

    response_note = ""
    if severity in {"HIGH", "CRITICAL"}:
        check_and_block(target, severity)
        response_note = " Simulated IPS decision recorded (no firewall rule was changed)."

    insert_alert(
        target,
        attack_name,
        severity,
        source="simulation",
        details=(output.strip() + response_note).strip() or "Controlled lab simulation completed.",
    )
    flash(f"{attack_name} completed for {target}.{response_note}", "success")
    return redirect(url_for("index"))


@app.post("/ingest-ids")
def ingest_ids():
    inserted = parse_logs(insert_alert)
    flash(f"IDS import finished: {inserted} new alert(s) imported.", "success")
    return redirect(url_for("index"))


@app.get("/health")
def health():
    # A lightweight local status endpoint; does not expose host or configuration data.
    return {"status": "ok", "database": "ready"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # Keep the development dashboard bound to loopback by default.
    app.run(host="127.0.0.1", port=port, debug=False)
