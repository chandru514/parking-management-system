"""
Parking Management System - Version 2 (v2)
Features:
- v1: Add Vehicle - Record vehicle entry
- v2: Exit Vehicle - Record exit time, duration & parking fee
Author: Chandru (Reg No: 24MIS0514)
"""

import os
import sqlite3
import math
from datetime import datetime
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "parking_v2.db")

RATE_CARD = {
    "Two Wheeler": 20,
    "Car": 40,
    "SUV / Heavy": 60
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            duration_minutes INTEGER DEFAULT 0,
            fee REAL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'PARKED'
        )
    """)
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parking Management System - v2</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(148, 163, 184, 0.15);
            --primary: #a855f7;
            --primary-hover: #9333ea;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body {
            background: linear-gradient(135deg, #090d16 0%, #1e1035 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 980px;
        }
        .header {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        .version-badge {
            display: inline-block;
            background: rgba(168, 85, 247, 0.2);
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            border: 1px solid rgba(168, 85, 247, 0.3);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .header h1 {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 6px;
            background: linear-gradient(to right, #ffffff, #d8b4fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }
        .meta-info {
            margin-top: 10px;
            font-size: 0.85rem;
            color: #c084fc;
            font-weight: 500;
        }
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: 2fr 1.5fr auto;
            gap: 12px;
            align-items: end;
        }
        @media (max-width: 650px) {
            .form-grid { grid-template-columns: 1fr; }
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        label {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        input, select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }
        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
        }
        button.btn-primary {
            background: var(--primary);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 11px 22px;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s;
            height: 42px;
        }
        button.btn-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }
        .btn-exit {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: 600;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-exit:hover {
            background: #ef4444;
            color: #fff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            text-align: left;
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }
        th {
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-parked {
            background: rgba(34, 197, 94, 0.15);
            color: var(--success);
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .badge-exited {
            background: rgba(148, 163, 184, 0.15);
            color: var(--text-muted);
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        .empty-state {
            text-align: center;
            padding: 30px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="version-badge">Version 2.0 (v2)</span>
            <h1>Parking Management System</h1>
            <p>Features: Entry (v1) &amp; Exit Vehicle Record (v2)</p>
            <div class="meta-info">Student Reg No: <strong>24MIS0514</strong> | Candidate: Chandru</div>
        </div>

        <div class="card">
            <div class="card-title">
                <span>🚗</span> Record Vehicle Entry
            </div>
            <form method="POST" action="/add" class="form-grid">
                <div class="form-group">
                    <label for="vehicle_number">Vehicle Plate Number</label>
                    <input type="text" id="vehicle_number" name="vehicle_number" placeholder="e.g. TN-07-BW-1234" required>
                </div>
                <div class="form-group">
                    <label for="vehicle_type">Vehicle Type</label>
                    <select id="vehicle_type" name="vehicle_type">
                        <option value="Car">Car (₹40/hr)</option>
                        <option value="Two Wheeler">Two Wheeler (₹20/hr)</option>
                        <option value="SUV / Heavy">SUV / Heavy (₹60/hr)</option>
                    </select>
                </div>
                <button type="submit" class="btn-primary">+ Add Vehicle</button>
            </form>
        </div>

        <div class="card">
            <div class="card-title">
                <span>⏱️</span> Vehicle Parking &amp; Exit Management
            </div>
            {% if vehicles %}
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Vehicle</th>
                        <th>Type</th>
                        <th>Entry Time</th>
                        <th>Exit Time</th>
                        <th>Duration</th>
                        <th>Fee</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for v in vehicles %}
                    <tr>
                        <td>{{ v[0] }}</td>
                        <td><strong>{{ v[1] }}</strong></td>
                        <td>{{ v[2] }}</td>
                        <td>{{ v[3] }}</td>
                        <td>{{ v[4] if v[4] else '—' }}</td>
                        <td>{{ v[5] ~ ' mins' if v[4] else 'In Progress' }}</td>
                        <td>{{ '₹' ~ "%.2f"|format(v[6]) if v[4] else '—' }}</td>
                        <td>
                            {% if v[7] == 'PARKED' %}
                                <span class="badge badge-parked">PARKED</span>
                            {% else %}
                                <span class="badge badge-exited">EXITED</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if v[7] == 'PARKED' %}
                            <form method="POST" action="/exit/{{ v[0] }}" style="display:inline;">
                                <button type="submit" class="btn-exit">Record Exit</button>
                            </form>
                            {% else %}
                            <span style="color: var(--text-muted); font-size: 0.8rem;">Completed</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                No vehicles recorded. Add an entry above.
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, vehicle_number, vehicle_type, entry_time, exit_time, duration_minutes, fee, status
        FROM vehicles ORDER BY id DESC
    """)
    vehicles = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, vehicles=vehicles)

@app.route("/add", methods=["POST"])
def add_vehicle():
    num = request.form.get("vehicle_number", "").strip().upper()
    v_type = request.form.get("vehicle_type", "Car")
    if num:
        entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vehicles (vehicle_number, vehicle_type, entry_time, status) VALUES (?, ?, ?, 'PARKED')",
            (num, v_type, entry)
        )
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/exit/<int:vehicle_id>", methods=["POST"])
def exit_vehicle(vehicle_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT entry_time, vehicle_type, status FROM vehicles WHERE id = ?", (vehicle_id,))
    row = cursor.fetchone()

    if row and row[2] == "PARKED":
        entry_time_str = row[0]
        vehicle_type = row[1]
        now = datetime.now()
        exit_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        entry_dt = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        diff_seconds = max(60, int((now - entry_dt).total_seconds()))
        duration_minutes = math.ceil(diff_seconds / 60)

        rate_per_hour = RATE_CARD.get(vehicle_type, 40)
        hours = max(1, math.ceil(duration_minutes / 60))
        fee = hours * rate_per_hour

        cursor.execute("""
            UPDATE vehicles
            SET exit_time = ?, duration_minutes = ?, fee = ?, status = 'EXITED'
            WHERE id = ?
        """, (exit_time_str, duration_minutes, fee, vehicle_id))
        conn.commit()

    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5002))
    print(f"Parking System v2 running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
