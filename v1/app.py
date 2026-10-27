"""
Parking Management System - Version 1 (v1)
Feature: Add Vehicle - Record vehicle entry
Author: Chandru (Reg No: 24MIS0514)
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "parking_v1.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT NOT NULL,
            vehicle_type TEXT NOT NULL,
            entry_time TEXT NOT NULL,
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
    <title>Parking Management System - v1</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(148, 163, 184, 0.15);
            --primary: #38bdf8;
            --primary-hover: #0ea5e9;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #22c55e;
            --badge-bg: rgba(34, 197, 94, 0.15);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 900px;
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
            position: relative;
        }
        .version-badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.2);
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            border: 1px solid rgba(56, 189, 248, 0.3);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .header h1 {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 6px;
            background: linear-gradient(to right, #ffffff, #93c5fd);
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
            color: #38bdf8;
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
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }
        button.btn-primary {
            background: var(--primary);
            color: #0f172a;
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
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            text-align: left;
            padding: 12px 16px;
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
            background: var(--badge-bg);
            color: var(--success);
            border: 1px solid rgba(34, 197, 94, 0.3);
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
            <span class="version-badge">Version 1.0 (v1)</span>
            <h1>Parking Management System</h1>
            <p>Feature: Record Vehicle Entry (Add Vehicle)</p>
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
                        <option value="Car">Car</option>
                        <option value="Two Wheeler">Two Wheeler</option>
                        <option value="SUV / Heavy">SUV / Heavy</option>
                    </select>
                </div>
                <button type="submit" class="btn-primary">+ Add Vehicle</button>
            </form>
        </div>

        <div class="card">
            <div class="card-title">
                <span>📋</span> Currently Parked Vehicles ({{ vehicles|length }})
            </div>
            {% if vehicles %}
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Vehicle Number</th>
                        <th>Type</th>
                        <th>Entry Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for v in vehicles %}
                    <tr>
                        <td>{{ v[0] }}</td>
                        <td><strong>{{ v[1] }}</strong></td>
                        <td>{{ v[2] }}</td>
                        <td>{{ v[3] }}</td>
                        <td><span class="badge badge-parked">{{ v[4] }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                No vehicles entered yet. Use the form above to record vehicle entry.
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
    cursor.execute("SELECT id, vehicle_number, vehicle_type, entry_time, status FROM vehicles ORDER BY id DESC")
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

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5001))
    print(f"Parking System v1 running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
