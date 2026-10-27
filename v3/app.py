"""
Parking Management System - Version 3 (v3)
Features:
- v1: Add Vehicle - Record vehicle entry
- v2: Exit Vehicle - Record exit time, duration & fee
- v3: View Records - Comprehensive parking history & analytical dashboard
Author: Chandru (Reg No: 24MIS0514)
"""

import os
import sqlite3
import math
from datetime import datetime
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "parking_v3.db")

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
    <title>Parking Management System - v3</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --card-bg: rgba(22, 30, 49, 0.75);
            --border: rgba(148, 163, 184, 0.14);
            --primary: #38bdf8;
            --primary-hover: #0ea5e9;
            --accent: #6366f1;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --danger: #f43f5e;
            --warning: #f59e0b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body {
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0b0f19 75%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 1100px;
        }
        .header {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 26px;
            margin-bottom: 24px;
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        .version-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            color: #818cf8;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 5px 14px;
            border-radius: 9999px;
            border: 1px solid rgba(99, 102, 241, 0.35);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .header h1 {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }
        .meta-info {
            margin-top: 12px;
            font-size: 0.85rem;
            color: #38bdf8;
            font-weight: 600;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        @media (max-width: 800px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .stat-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.3);
        }
        .stat-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .stat-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: #fff;
        }
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(14px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.3);
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
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
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 500;
        }
        input, select {
            background: rgba(11, 15, 25, 0.7);
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
            background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
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
            opacity: 0.95;
            transform: translateY(-1px);
        }
        .btn-exit {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.3);
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: 600;
            font-size: 0.78rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-exit:hover {
            background: #f43f5e;
            color: #fff;
        }
        .filter-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
            align-items: center;
            background: rgba(11, 15, 25, 0.4);
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid var(--border);
        }
        .filter-bar input {
            flex: 1;
            min-width: 180px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 6px;
        }
        th, td {
            text-align: left;
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            font-size: 0.88rem;
        }
        th {
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.03em;
        }
        .badge-parked {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-exited {
            background: rgba(148, 163, 184, 0.15);
            color: #94a3b8;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        .empty-state {
            text-align: center;
            padding: 35px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="version-badge">Version 3.0 (v3) - Complete Suite</span>
            <h1>Parking Management System</h1>
            <p>Features: Entry (v1) | Exit (v2) | Complete Parking History &amp; Analytics (v3)</p>
            <div class="meta-info">Student Reg No: <strong>24MIS0514</strong> | Candidate: Chandru</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Recorded</div>
                <div class="stat-value">{{ stats.total }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Currently Parked</div>
                <div class="stat-value" style="color: #34d399;">{{ stats.parked }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Exited Vehicles</div>
                <div class="stat-value" style="color: #94a3b8;">{{ stats.exited }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Revenue Collected</div>
                <div class="stat-value" style="color: #38bdf8;">₹{{ "%.2f"|format(stats.revenue) }}</div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                <span>🚗</span> Record Vehicle Entry (v1)
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
                <span>📊</span> Parking History Records &amp; Filter (v3)
            </div>

            <form method="GET" action="/" class="filter-bar">
                <input type="text" name="search" placeholder="Search Vehicle Plate..." value="{{ search_query }}">
                <select name="status">
                    <option value="" {% if not filter_status %}selected{% endif %}>All Statuses</option>
                    <option value="PARKED" {% if filter_status == 'PARKED' %}selected{% endif %}>Currently Parked</option>
                    <option value="EXITED" {% if filter_status == 'EXITED' %}selected{% endif %}>Exited</option>
                </select>
                <select name="vtype">
                    <option value="" {% if not filter_vtype %}selected{% endif %}>All Vehicle Types</option>
                    <option value="Car" {% if filter_vtype == 'Car' %}selected{% endif %}>Car</option>
                    <option value="Two Wheeler" {% if filter_vtype == 'Two Wheeler' %}selected{% endif %}>Two Wheeler</option>
                    <option value="SUV / Heavy" {% if filter_vtype == 'SUV / Heavy' %}selected{% endif %}>SUV / Heavy</option>
                </select>
                <button type="submit" class="btn-primary" style="height: 38px; padding: 0 16px;">Filter</button>
                {% if search_query or filter_status or filter_vtype %}
                <a href="/" style="color: var(--text-muted); font-size: 0.85rem; text-decoration: none;">Clear Filter</a>
                {% endif %}
            </form>

            {% if vehicles %}
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Vehicle Number</th>
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
                        <td>{{ v[5] ~ ' mins' if v[4] else 'Active' }}</td>
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
                            <span style="color: var(--text-muted); font-size: 0.8rem;">Finished</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                No matching parking records found.
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    search = request.args.get("search", "").strip().upper()
    status = request.args.get("status", "").strip()
    vtype = request.args.get("vtype", "").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT id, vehicle_number, vehicle_type, entry_time, exit_time, duration_minutes, fee, status FROM vehicles WHERE 1=1"
    params = []

    if search:
        query += " AND vehicle_number LIKE ?"
        params.append(f"%{search}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if vtype:
        query += " AND vehicle_type = ?"
        params.append(vtype)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    vehicles = cursor.fetchall()

    # Calculate statistics
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status = 'PARKED'")
    parked = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status = 'EXITED'")
    exited = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(fee) FROM vehicles WHERE status = 'EXITED'")
    rev_row = cursor.fetchone()[0]
    revenue = rev_row if rev_row else 0.0

    conn.close()

    stats = {
        "total": total,
        "parked": parked,
        "exited": exited,
        "revenue": revenue
    }

    return render_template_string(
        HTML_TEMPLATE,
        vehicles=vehicles,
        stats=stats,
        search_query=search,
        filter_status=status,
        filter_vtype=vtype
    )

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
    port = int(os.environ.get("PORT", 5003))
    print(f"Parking System v3 running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
