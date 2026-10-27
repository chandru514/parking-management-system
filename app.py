"""
Parking Management System - Roll No: 24MIS0514
Course: Agile Development Process and DevOps Lab

Features:
- v1: Add Vehicle - Record vehicle entry
- v2: Exit Vehicle - Record exit time, duration, and fee calculation
- v3: View Records - Complete history, searching, filtering & dashboard metrics

Run locally:
python app.py
"""

from v3.app import app, init_db
import os

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"Parking Management System (24MIS0514) running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
