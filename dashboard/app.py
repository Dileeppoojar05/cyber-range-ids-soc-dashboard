from flask import Flask, request, redirect, render_template
import subprocess
import sys
import os

sys.path.append("../")

from database.db import init_db, insert_alert, fetch_alerts
from response.ips import check_and_block
from flask import render_template
from ids.ids_parser import parse_logs

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    alerts = fetch_alerts()
    return render_template("index.html", alerts=alerts)

@app.route("/attack", methods=["POST"])
def attack():
    target = request.form["target"]
    attack_type = request.form["attack_type"]

    script_map = {
        "scan": "../red_team/port_scanner.py",
        "brute": "../red_team/brute_force.py",
        "web": "../red_team/web_attacks.py",
        "ddos": "../red_team/ddos_simulator.py"
    }

    script = script_map.get(attack_type)

    if script:
        subprocess.Popen(["python", script, target])

        # Simulated detection before IDS kicks in
        severity = "HIGH" if attack_type in ["ddos", "brute"] else "MEDIUM"

        insert_alert(target, attack_type, severity)
        check_and_block(target, severity)

    # 🔥 CRITICAL: Parse IDS logs after attack
    parse_logs(insert_alert)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
