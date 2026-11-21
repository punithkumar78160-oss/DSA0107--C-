import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import datetime
import webbrowser

# Local imports
import cpp_bridge
import database

# ============================================================================
# INSTANT ZERO-DEPENDENCY WEB SERVER FOR BUS PASS AUTOMATION SYSTEM
# Launches instantly in under 1 second without needing any pip installs!
# White Background (#FFFFFF) | Black Font (#000000) | Clear Dropdown Menus
# ============================================================================

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bus Pass Automation System | Saveetha Institute</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.5;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            border-bottom: 2px solid #000000;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }
        h1 { font-size: 28px; color: #000000; }
        .subtitle { font-size: 15px; color: #333333; margin-top: 4px; }
        .credits {
            background-color: #F8FAFC;
            border: 1px solid #000000;
            border-radius: 6px;
            padding: 10px 16px;
            font-size: 13px;
            margin-top: 10px;
        }
        .metrics-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .metric-card {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 8px;
            padding: 14px;
            box-shadow: 3px 3px 0px #000000;
        }
        .metric-card h3 { font-size: 13px; color: #4B5563; text-transform: uppercase; }
        .metric-card p { font-size: 26px; font-weight: 800; color: #000000; margin-top: 5px; }
        
        /* Tabs */
        .tabs { display: flex; gap: 8px; border-bottom: 2px solid #000000; margin-bottom: 20px; flex-wrap: wrap; }
        .tab-btn {
            background-color: #F3F4F6;
            color: #000000;
            border: 2px solid #000000;
            border-bottom: none;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            border-radius: 6px 6px 0 0;
        }
        .tab-btn.active {
            background-color: #000000;
            color: #FFFFFF;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Form Controls - STRICT HIGH CONTRAST & VISIBLE DROPDOWNS */
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-weight: bold; margin-bottom: 6px; font-size: 14px; color: #000000; }
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 10px 12px;
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 600;
        }
        select option {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-size: 14px;
            padding: 8px;
        }
        .btn {
            background-color: #000000;
            color: #FFFFFF;
            border: 2px solid #000000;
            padding: 12px 24px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 3px 3px 0px #888888;
        }
        .btn:hover { background-color: #333333; }
        
        /* Cards & Badges */
        .card {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 4px 4px 0px #000000;
        }
        .badge-valid { background: #D1FAE5; color: #065F46; border: 2px solid #059669; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        .badge-expired { background: #FEE2E2; color: #991B1B; border: 2px solid #DC2626; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #000000; padding: 10px; text-align: left; font-size: 14px; color: #000000; }
        th { background-color: #F3F4F6; font-weight: bold; }
        pre { background: #1E1E1E; color: #39FF14; padding: 15px; border-radius: 6px; overflow-x: auto; font-family: monospace; }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>🚌 Bus Pass Automation System</h1>
        <div class="subtitle">Menu-Driven Architecture with File Handling & C++ OOP Core Engine</div>
        <div class="credits">
            <b>Team:</b> YOKAVISHWA A (192471017) | ELAMARAN S (192524246) | PUNITH KUMAR N (192525156)<br>
            <b>Guided By:</b> Mr Jegadeesh K (Industrial Professional, Coimbatore) | <b>College:</b> Saveetha Institute of Medical and Technical Sciences (SIMATS)
        </div>
    </header>

    <div class="metrics-row" id="metrics-bar">
        <div class="metric-card"><h3>Total Passes</h3><p id="m-total">-</p></div>
        <div class="metric-card"><h3>Active Passes</h3><p id="m-active" style="color:#059669;">-</p></div>
        <div class="metric-card"><h3>Expired Passes</h3><p id="m-expired" style="color:#DC2626;">-</p></div>
        <div class="metric-card"><h3>Expiring Soon</h3><p id="m-soon" style="color:#D97706;">-</p></div>
        <div class="metric-card"><h3>Total Revenue</h3><p id="m-revenue">-</p></div>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab(0)">📝 1. Register & Issue Pass</button>
        <button class="tab-btn" onclick="switchTab(1)">🔄 2. Renew Pass</button>
        <button class="tab-btn" onclick="switchTab(2)">🔍 3. Validate Pass</button>
        <button class="tab-btn" onclick="switchTab(3)">📊 4. Summary & Reports</button>
        <button class="tab-btn" onclick="switchTab(4)">🗄️ 5. Database & CSV</button>
        <button class="tab-btn" onclick="switchTab(5)">⚙️ 6. C++ OOP Architecture</button>
    </div>

    <!-- TAB 1: ISSUE -->
    <div class="tab-content active" id="tab-0">
        <div class="card">
            <h2 style="margin-bottom:15px;">Module 1: Passenger Registration & Pass Issuance</h2>
            <div class="form-grid">
                <div>
                    <div class="form-group">
                        <label>Passenger Name *</label>
                        <input type="text" id="reg-name" value="Yokavishwa A">
                    </div>
                    <div class="form-group">
                        <label>Age *</label>
                        <input type="number" id="reg-age" value="21">
                    </div>
                    <div class="form-group">
                        <label>Category *</label>
                        <select id="reg-cat" onchange="updateFarePreview()">
                            <option value="Student">Student (70% Concession)</option>
                            <option value="General Commuter">General Commuter (Standard)</option>
                            <option value="Senior Citizen">Senior Citizen (50% Concession)</option>
                        </select>
                    </div>
                </div>
                <div>
                    <div class="form-group">
                        <label>Route Source *</label>
                        <select id="reg-from">
                            <option>Gandhipuram</option>
                            <option>Central Bus Stand</option>
                            <option>Singanallur</option>
                            <option>Ukkadam</option>
                            <option>Railway Junction</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Route Destination *</label>
                        <select id="reg-to">
                            <option>Saveetha Campus</option>
                            <option>Peelamedu / CIT</option>
                            <option>Town Hall</option>
                            <option>Saravanampatti</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Duration *</label>
                        <select id="reg-duration" onchange="updateFarePreview()">
                            <option value="1">1 Month (Monthly)</option>
                            <option value="3" selected>3 Months (Quarterly)</option>
                            <option value="12">12 Months (Annual)</option>
                        </select>
                    </div>
                    <div style="background:#F1F5F9; border:2px dashed #000; padding:12px; border-radius:6px; margin-bottom:15px;">
                        <b>C++ Fare Calculation: </b><span id="fare-preview" style="font-size:20px; font-weight:800; color:#000;">Rs. 450.00</span>
                    </div>
                </div>
            </div>
            <button class="btn" onclick="submitIssuePass()">🚀 Register & Issue Pass (C++ Engine)</button>
            <div id="issue-result" style="margin-top:15px;"></div>
        </div>
    </div>

    <!-- TAB 2: RENEW -->
    <div class="tab-content" id="tab-1">
        <div class="card">
            <h2 style="margin-bottom:15px;">Module 2: Pass Renewal (Atomic File Swap)</h2>
            <div class="form-group">
                <label>Select Pass ID to Renew *</label>
                <select id="renew-pass-select"></select>
            </div>
            <div class="form-group">
                <label>Renewal Extension (Months) *</label>
                <select id="renew-months">
                    <option value="1">1 Month</option>
                    <option value="3" selected>3 Months</option>
                    <option value="6">6 Months</option>
                    <option value="12">12 Months</option>
                </select>
            </div>
            <button class="btn" onclick="submitRenewPass()">🔄 Execute Pass Renewal</button>
            <div id="renew-result" style="margin-top:15px;"></div>
        </div>
    </div>

    <!-- TAB 3: VALIDATE -->
    <div class="tab-content" id="tab-2">
        <div class="card">
            <h2 style="margin-bottom:15px;">Module 2: Pass Validation (Slide 8 & 9)</h2>
            <div class="form-group">
                <label>Enter Pass ID to Validate *</label>
                <input type="text" id="val-pass-id" value="BP1001" placeholder="e.g. BP1001">
            </div>
            <button class="btn" onclick="submitValidatePass()">🔍 Check Pass Validity</button>
            <div id="validate-result" style="margin-top:15px;"></div>
        </div>
    </div>

    <!-- TAB 4: SUMMARY & REPORTS -->
    <div class="tab-content" id="tab-3">
        <div class="card">
            <h2 style="margin-bottom:15px;">Module 2: Summary Report & Analytics</h2>
            <p>Direct view of <b>report.txt</b> as generated by the C++ engine:</p>
            <pre id="report-text-view" style="margin-top:10px;">Loading report.txt...</pre>
            <button class="btn" style="margin-top:15px;" onclick="loadReport()">📄 Refresh report.txt</button>
        </div>
    </div>

    <!-- TAB 5: DATABASE & CSV -->
    <div class="tab-content" id="tab-4">
        <div class="card">
            <h2 style="margin-bottom:15px;">Database (bus_pass.db) & CSV Storage (passes.csv)</h2>
            <table id="passes-table">
                <thead>
                    <tr><th>Pass ID</th><th>Name</th><th>Expiry Date</th><th>Route</th><th>Category</th><th>Fare</th><th>Status</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <!-- TAB 6: C++ ARCHITECTURE -->
    <div class="tab-content" id="tab-5">
        <div class="card">
            <h2>C++ Object-Oriented Programming Architecture</h2>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><b>Encapsulation:</b> Class <code>Passenger</code> and <code>BusPass</code> with private data members and safe public getters.</li>
                <li><b>Inheritance:</b> Derived classes <code>StudentPass</code>, <code>CommuterPass</code>, and <code>SeniorCitizenPass</code> inheriting from base <code>BusPass</code>.</li>
                <li><b>Polymorphism:</b> Pure virtual functions <code>calculateFare()</code> implementing 70% concession for students and 50% for senior citizens.</li>
                <li><b>File Handling:</b> Atomic file replacement using <code>passes.csv.tmp</code> replaced cleanly with <code>passes.csv</code>.</li>
            </ul>
        </div>
    </div>
</div>

<script>
    function switchTab(index) {
        document.querySelectorAll('.tab-btn').forEach((btn, i) => btn.classList.toggle('active', i === index));
        document.querySelectorAll('.tab-content').forEach((tab, i) => tab.classList.toggle('active', i === index));
    }

    function updateFarePreview() {
        const cat = document.getElementById('reg-cat').value;
        const months = parseInt(document.getElementById('reg-duration').value);
        let fare = 500.0 * months;
        if (cat === 'Student') fare *= 0.30;
        else if (cat === 'Senior Citizen') fare *= 0.50;
        document.getElementById('fare-preview').innerText = 'Rs. ' + fare.toFixed(2);
    }

    async function loadData() {
        const res = await fetch('/api/data');
        const data = await res.json();
        
        document.getElementById('m-total').innerText = data.summary.total;
        document.getElementById('m-active').innerText = data.summary.active;
        document.getElementById('m-expired').innerText = data.summary.expired;
        document.getElementById('m-soon').innerText = data.summary.expiring_soon || 0;
        document.getElementById('m-revenue').innerText = 'Rs. ' + data.summary.revenue.toFixed(2);

        // Populate table & dropdown
        const tbody = document.querySelector('#passes-table tbody');
        const select = document.getElementById('renew-pass-select');
        tbody.innerHTML = '';
        select.innerHTML = '';

        data.passes.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td><b>${p.pass_id}</b></td><td>${p.name}</td><td>${p.expiry_date}</td><td>${p.route_from} ➔ ${p.route_to}</td><td>${p.category}</td><td>Rs. ${p.fare}</td><td><span class="${p.status === 'VALID' ? 'badge-valid' : 'badge-expired'}">${p.status}</span></td>`;
            tbody.appendChild(tr);

            const opt = document.createElement('option');
            opt.value = p.pass_id;
            opt.innerText = `${p.pass_id} - ${p.name} (${p.status})`;
            select.appendChild(opt);
        });

        loadReport();
    }

    async function submitIssuePass() {
        const payload = {
            name: document.getElementById('reg-name').value,
            age: parseInt(document.getElementById('reg-age').value),
            category: document.getElementById('reg-cat').value,
            route_from: document.getElementById('reg-from').value,
            route_to: document.getElementById('reg-to').value,
            duration: parseInt(document.getElementById('reg-duration').value)
        };
        const res = await fetch('/api/issue', { method: 'POST', body: JSON.stringify(payload) });
        const data = await res.json();
        document.getElementById('issue-result').innerHTML = `<div class="card" style="background:#D1FAE5; border-color:#059669;"><b>Success:</b> Pass <b>${data.pass_id}</b> issued for <b>${data.name}</b> until <b>${data.expiry}</b>! Saved to passes.csv.</div>`;
        loadData();
    }

    async function submitRenewPass() {
        const pass_id = document.getElementById('renew-pass-select').value;
        const months = parseInt(document.getElementById('renew-months').value);
        const res = await fetch('/api/renew', { method: 'POST', body: JSON.stringify({ pass_id, months }) });
        const data = await res.json();
        document.getElementById('renew-result').innerHTML = `<div class="card" style="background:#D1FAE5; border-color:#059669;"><b>Success:</b> Pass <b>${pass_id}</b> renewed until <b>${data.new_expiry}</b>!</div>`;
        loadData();
    }

    async function submitValidatePass() {
        const pass_id = document.getElementById('val-pass-id').value;
        const res = await fetch('/api/validate?id=' + encodeURIComponent(pass_id));
        const data = await res.json();
        if (data.found) {
            const badge = data.status === 'VALID' ? '<span class="badge-valid">STATUS: VALID</span>' : '<span class="badge-expired">STATUS: EXPIRED</span>';
            document.getElementById('validate-result').innerHTML = `<div class="card"><h3>${data.name} (${data.pass_id})</h3><p style="margin:10px 0;">${badge} &nbsp; <b>Expires:</b> ${data.expiry} (${data.days_remaining} days)</p></div>`;
        } else {
            document.getElementById('validate-result').innerHTML = `<div class="card" style="background:#FEE2E2; border-color:#DC2626;"><b>Error:</b> ${data.error}</div>`;
        }
    }

    async function loadReport() {
        const res = await fetch('/api/report');
        const text = await res.text();
        document.getElementById('report-text-view').innerText = text;
    }

    updateFarePreview();
    loadData();
</script>
</body>
</html>
"""

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/data":
            passes = cpp_bridge.cpp_get_all_passes()
            summary = cpp_bridge.cpp_get_summary()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"passes": passes, "summary": summary}).encode("utf-8"))
        elif parsed.path == "/api/validate":
            query = urllib.parse.parse_qs(parsed.query)
            pass_id = query.get("id", [""])[0]
            val = cpp_bridge.cpp_validate_pass(pass_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(val).encode("utf-8"))
        elif parsed.path == "/api/report":
            content = "No report available."
            if os.path.exists("report.txt"):
                with open("report.txt", "r", encoding="utf-8") as f:
                    content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        data = json.loads(body) if body else {}

        if parsed.path == "/api/issue":
            res = cpp_bridge.cpp_issue_pass(
                name=data.get("name", ""),
                age=data.get("age", 21),
                route_from=data.get("route_from", "Central"),
                route_to=data.get("route_to", "Campus"),
                pass_type="Monthly",
                duration_months=data.get("duration", 1),
                category=data.get("category", "")
            )
            database.db_insert_pass(
                pass_id=res["pass_id"],
                passenger_id=res["passenger_id"],
                name=data.get("name", ""),
                age=data.get("age", 21),
                r_from=data.get("route_from", "Central"),
                r_to=data.get("route_to", "Campus"),
                issue_date=str(datetime.date.today()),
                expiry_date=res["expiry"],
                pass_type="Monthly",
                category=data.get("category", ""),
                fare=res["fare"]
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/renew":
            pass_id = data.get("pass_id", "")
            months = data.get("months", 3)
            res = cpp_bridge.cpp_renew_pass(pass_id, months)
            if res.get("success"):
                database.db_renew_pass(pass_id, months, res["new_expiry"])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

def start_server(port=8501):
    # Try finding an open port
    for p in range(port, port + 20):
        try:
            with socketserver.TCPServer(("", p), RequestHandler) as httpd:
                print(f"[OK] Bus Pass Automation System running on: http://localhost:{p}")
                webbrowser.open(f"http://localhost:{p}")
                httpd.serve_forever()
                return
        except OSError:
            print(f"[!] Port {p} is busy. Trying alternate port {p + 1}...")

if __name__ == "__main__":
    start_port = 8501
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        start_port = int(sys.argv[1])
    start_server(start_port)
