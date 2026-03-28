#!/usr/bin/env python3
# ============================================================
#  app.py — Optional Flask Web Dashboard
# ============================================================
#
#  USAGE:
#      python app.py
#      Visit: http://localhost:5000
# ============================================================

from flask import Flask, render_template_string, jsonify
from automation.attendance import get_todays_report, export_to_excel
import os

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Vision Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; }
    header { background: #1e293b; padding: 20px 40px; display: flex; align-items: center; gap: 12px; }
    header h1 { font-size: 1.5rem; color: #38bdf8; }
    .badge { background: #22c55e; color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; }
    main { padding: 40px; }
    .stats { display: flex; gap: 20px; margin-bottom: 40px; flex-wrap: wrap; }
    .card { background: #1e293b; border-radius: 12px; padding: 24px; flex: 1; min-width: 180px; }
    .card .label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .card .value { font-size: 2.2rem; font-weight: 700; color: #38bdf8; margin-top: 8px; }
    table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }
    th { background: #0f172a; padding: 14px 18px; text-align: left; font-size: 0.8rem;
         text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; }
    td { padding: 14px 18px; border-top: 1px solid #334155; font-size: 0.9rem; }
    tr:hover td { background: #263551; }
    .present { color: #22c55e; font-weight: 600; }
    .section-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; color: #cbd5e1; }
    .export-btn { margin-top: 20px; background: #0ea5e9; color: white; border: none;
                  padding: 10px 24px; border-radius: 8px; cursor: pointer; font-size: 0.9rem; }
    .export-btn:hover { background: #0284c7; }
  </style>
</head>
<body>
  <header>
    <h1>🔍 Smart Vision</h1>
    <span class="badge">Live</span>
  </header>
  <main>
    <div class="stats">
      <div class="card">
        <div class="label">Present Today</div>
        <div class="value" id="presentCount">—</div>
      </div>
      <div class="card">
        <div class="label">Total Entries</div>
        <div class="value" id="totalCount">—</div>
      </div>
    </div>

    <div class="section-title">Today's Attendance</div>
    <table>
      <thead>
        <tr>
          <th>#</th><th>Name</th><th>Date</th><th>Time</th><th>Status</th>
        </tr>
      </thead>
      <tbody id="attendanceBody">
        <tr><td colspan="5" style="text-align:center;color:#64748b;">Loading...</td></tr>
      </tbody>
    </table>
    <button class="export-btn" onclick="exportExcel()">⬇ Export to Excel</button>
  </main>

  <script>
    async function loadData() {
      const res  = await fetch('/api/attendance');
      const data = await res.json();
      const tbody = document.getElementById('attendanceBody');
      tbody.innerHTML = '';
      if (!data.length) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#64748b;">No records yet.</td></tr>';
        return;
      }
      data.forEach((row, i) => {
        tbody.innerHTML += `<tr>
          <td>${i+1}</td>
          <td>${row.Name}</td>
          <td>${row.Date}</td>
          <td>${row.Time}</td>
          <td class="present">${row.Status}</td>
        </tr>`;
      });
      document.getElementById('presentCount').textContent = new Set(data.map(r=>r.Name)).size;
      document.getElementById('totalCount').textContent   = data.length;
    }
    async function exportExcel() {
      await fetch('/api/export');
      alert('Exported to logs/attendance_report.xlsx');
    }
    loadData();
    setInterval(loadData, 5000);  // Auto-refresh every 5 seconds
  </script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/attendance")
def api_attendance():
    df = get_todays_report()
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/export")
def api_export():
    export_to_excel()
    return jsonify({"status": "exported"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
