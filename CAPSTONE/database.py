import sqlite3
import os
import csv
import datetime
from typing import List, Dict, Any

# ============================================================================
# DATABASE ENGINE FOR BUS PASS AUTOMATION SYSTEM
# Relational SQLite backend synchronized with CSV File Handling (passes.csv)
# ============================================================================

DB_FILE = "bus_pass.db"
CSV_FILE = "passes.csv"
REPORT_FILE = "report.txt"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initializes tables and seeds initial data matching PPT demonstration."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        category TEXT NOT NULL,
        contact TEXT DEFAULT ''
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passes (
        pass_id TEXT PRIMARY KEY,
        passenger_id TEXT NOT NULL,
        name TEXT NOT NULL,
        route_from TEXT NOT NULL,
        route_to TEXT NOT NULL,
        issue_date TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        pass_type TEXT NOT NULL,
        category TEXT NOT NULL,
        fare REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS renewal_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pass_id TEXT NOT NULL,
        renewal_date TEXT NOT NULL,
        months_added INTEGER NOT NULL,
        new_expiry TEXT NOT NULL
    )
    """)
    conn.commit()

    # Sync from CSV or seed sample records if empty
    cursor.execute("SELECT COUNT(*) FROM passes")
    count = cursor.fetchone()[0]

    if count == 0:
        if os.path.exists(CSV_FILE):
            sync_db_from_csv()
        else:
            seed_sample_records()
            sync_csv_from_db()
    conn.close()

def seed_sample_records():
    """Seeds the demonstration records matching PPT slides (BP1001, 128 total passes stats)."""
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.date.today()
    sample_data = [
        ("BP1001", "P101", "Yokavishwa A", 21, "Gandhipuram", "Saveetha Campus", str(today - datetime.timedelta(days=30)), "2027-03-31", "Monthly", "Student", 150.0),
        ("BP1002", "P102", "Elamaran S", 21, "Central Bus Stand", "Peelamedu", str(today - datetime.timedelta(days=15)), str(today + datetime.timedelta(days=75)), "Quarterly", "Student", 450.0),
        ("BP1003", "P103", "Punith Kumar N", 22, "Singanallur", "Ukkadam", str(today - datetime.timedelta(days=60)), str(today + datetime.timedelta(days=120)), "Quarterly", "Student", 450.0),
        ("BP1004", "P104", "Dr. Jegadeesh K", 42, "RS Puram", "Gandhipuram", str(today - datetime.timedelta(days=10)), str(today + datetime.timedelta(days=20)), "Monthly", "General Commuter", 500.0),
        ("BP1005", "P105", "S. Ramanathan", 65, "Railway Junction", "Saravanampatti", str(today - datetime.timedelta(days=100)), str(today - datetime.timedelta(days=10)), "Annual", "Senior Citizen", 250.0), # Expired
        ("BP1006", "P106", "K. Priya", 20, "Hope College", "Saveetha Campus", str(today - datetime.timedelta(days=25)), str(today + datetime.timedelta(days=5)), "Monthly", "Student", 150.0), # Expiring soon
        ("BP1007", "P107", "M. Karthik", 35, "Sundarapuram", "Town Hall", str(today - datetime.timedelta(days=40)), str(today - datetime.timedelta(days=5)), "Monthly", "General Commuter", 500.0), # Expired
    ]

    for pass_id, p_id, name, age, r_from, r_to, iss, exp, p_type, cat, fare in sample_data:
        exp_date = datetime.date.fromisoformat(exp)
        status = "EXPIRED" if exp_date < today else ("EXPIRING_SOON" if (exp_date - today).days <= 7 else "VALID")
        
        cursor.execute("INSERT OR IGNORE INTO passengers VALUES (?, ?, ?, ?, ?)",
                       (p_id, name, age, cat, "9876543210"))
        cursor.execute("INSERT OR REPLACE INTO passes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (pass_id, p_id, name, r_from, r_to, iss, exp, p_type, cat, fare, status))

    conn.commit()
    conn.close()

def sync_csv_from_db():
    """Writes all current passes from SQLite into passes.csv to satisfy PPT Module 1 & 2 file handling."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pass_id, name, expiry_date, passenger_id, route_from, route_to, issue_date, pass_type, category, fare FROM passes")
    rows = cursor.fetchall()
    conn.close()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pass_id", "name", "expiry", "passenger_id", "route_from", "route_to", "issue_date", "pass_type", "category", "fare"])
        for r in rows:
            writer.writerow(list(r))

def sync_db_from_csv():
    """Reads passes.csv and updates SQLite database."""
    if not os.path.exists(CSV_FILE):
        return
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today()

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get("pass_id", "").strip()
            name = row.get("name", "").strip()
            exp_str = row.get("expiry", "").strip()
            passenger_id = row.get("passenger_id", f"P{pid[2:]}" if len(pid) > 2 else "P101")
            r_from = row.get("route_from", "Central")
            r_to = row.get("route_to", "Campus")
            issue_date = row.get("issue_date", str(today))
            p_type = row.get("pass_type", "Monthly")
            cat = row.get("category", "General Commuter")
            try:
                fare = float(row.get("fare", 500.0))
            except Exception:
                fare = 500.0

            try:
                exp_date = datetime.date.fromisoformat(exp_str)
                status = "EXPIRED" if exp_date < today else ("EXPIRING_SOON" if (exp_date - today).days <= 7 else "VALID")
            except Exception:
                status = "VALID"

            cursor.execute("INSERT OR IGNORE INTO passengers VALUES (?, ?, ?, ?, ?)",
                           (passenger_id, name, 21, cat, ""))
            cursor.execute("INSERT OR REPLACE INTO passes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (pid, passenger_id, name, r_from, r_to, issue_date, exp_str, p_type, cat, fare, status))
    conn.commit()
    conn.close()

def db_get_all_passes() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passes ORDER BY pass_id ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def db_search_passes(query: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    q = f"%{query.strip()}%"
    cursor.execute("""
        SELECT * FROM passes 
        WHERE pass_id LIKE ? OR name LIKE ? OR passenger_id LIKE ? OR route_from LIKE ? OR route_to LIKE ?
        ORDER BY pass_id ASC
    """, (q, q, q, q, q))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def db_insert_pass(pass_id, passenger_id, name, age, r_from, r_to, issue_date, expiry_date, pass_type, category, fare):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today()
    exp_date = datetime.date.fromisoformat(expiry_date)
    status = "EXPIRED" if exp_date < today else ("EXPIRING_SOON" if (exp_date - today).days <= 7 else "VALID")

    cursor.execute("INSERT OR REPLACE INTO passengers VALUES (?, ?, ?, ?, ?)",
                   (passenger_id, name, age, category, ""))
    cursor.execute("INSERT OR REPLACE INTO passes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (pass_id, passenger_id, name, r_from, r_to, issue_date, expiry_date, pass_type, category, fare, status))
    conn.commit()
    conn.close()
    sync_csv_from_db()

def db_renew_pass(pass_id, months_added, new_expiry):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today()
    exp_date = datetime.date.fromisoformat(new_expiry)
    status = "EXPIRED" if exp_date < today else ("EXPIRING_SOON" if (exp_date - today).days <= 7 else "VALID")

    cursor.execute("UPDATE passes SET expiry_date = ?, status = ? WHERE pass_id = ?",
                   (new_expiry, status, pass_id))
    cursor.execute("INSERT INTO renewal_logs (pass_id, renewal_date, months_added, new_expiry) VALUES (?, ?, ?, ?)",
                   (pass_id, str(today), months_added, new_expiry))
    conn.commit()
    conn.close()
    sync_csv_from_db()

# Initialize DB on first import
init_database()
