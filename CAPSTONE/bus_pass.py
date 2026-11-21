import os
import csv
import datetime
import shutil

# ============================================================================
# BUS PASS AUTOMATION SYSTEM - MENU-DRIVEN CONSOLE APPLICATION
# Matches Slides 6, 8, and 10 of PPT Presentation
# Team: YOKAVISHWA A (192471017), ELAMARAN S (192524246), PUNITH KUMAR N (192525156)
# Guide: Mr Jegadeesh K | Saveetha Institute of Medical and Technical Sciences
# ============================================================================

FILE = "passes.csv"
REPORT_FILE = "report.txt"

# Module 3: Menu Control & Error Handling
def check_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            f.write("pass_id,name,expiry,passenger_id,route_from,route_to,issue_date,pass_type,category,fare\n")
        print("passes.csv not found. New file created.")

def next_pass_id():
    check_file()
    max_id = 1000
    with open(FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row and len(row) > 0 and row[0].startswith("BP"):
                try:
                    num = int(row[0][2:])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    pass
    return f"BP{max_id + 1}"

def next_passenger_id():
    check_file()
    max_id = 100
    with open(FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row and len(row) > 3 and row[3].startswith("P"):
                try:
                    num = int(row[3][1:])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    pass
    return f"P{max_id + 1}"

# Module 1: Passenger Registration & Pass Issuance
def register_passenger(name, age):
    pass_id = next_pass_id()
    passenger_id = next_passenger_id()
    today = datetime.date.today()
    expiry = today + datetime.timedelta(days=365) # 1 year default
    fare = 150.0 if int(age) <= 24 else 500.0
    category = "Student" if int(age) <= 24 else "General Commuter"
    
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([pass_id, name, str(expiry), passenger_id, "Central", "Campus", str(today), "Monthly", category, f"{fare:.2f}"])
    return passenger_id, pass_id

def issue_bus_pass(passenger_id, name, duration_months=3):
    pass_id = next_pass_id()
    today = datetime.date.today()
    expiry = today + datetime.timedelta(days=duration_months * 30)
    fare = 450.0
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([pass_id, name, str(expiry), passenger_id, "Gandhipuram", "Saveetha Campus", str(today), "Quarterly", "Student", f"{fare:.2f}"])
    return pass_id

# Module 2: Pass Renewal, Validation & Reports
def renew_pass(pass_id, months=3):
    today = datetime.date.today()
    temp_file = FILE + ".tmp"
    found = False
    new_exp_str = ""

    # Flow: Read passes.csv into memory -> check expiry -> write to temp -> os.replace()
    with open(FILE, "r", newline="", encoding="utf-8") as src, open(temp_file, "w", newline="", encoding="utf-8") as dst:
        reader = csv.reader(src)
        writer = csv.writer(dst)
        header = next(reader, None)
        if header:
            writer.writerow(header)
        for row in reader:
            if row and len(row) >= 3 and row[0].strip().upper() == pass_id.strip().upper():
                found = True
                try:
                    curr_exp = datetime.date.fromisoformat(row[2])
                    base_date = curr_exp if curr_exp >= today else today
                    new_exp = base_date + datetime.timedelta(days=months * 30)
                    new_exp_str = str(new_exp)
                    row[2] = new_exp_str
                except Exception:
                    new_exp_str = str(today + datetime.timedelta(days=90))
                    row[2] = new_exp_str
            writer.writerow(row)

    if found:
        shutil.move(temp_file, FILE)
        return True, new_exp_str
    else:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False, ""

def validate_pass(pass_id):
    today = datetime.date.today()
    with open(FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row and len(row) >= 3 and row[0].strip().upper() == pass_id.strip().upper():
                try:
                    exp_date = datetime.date.fromisoformat(row[2])
                    status = "VALID" if exp_date >= today else "EXPIRED"
                    return True, status, row[2]
                except Exception:
                    return True, "VALID", row[2]
    return False, "NOT FOUND", ""

def view_summary_report():
    today = datetime.date.today()
    total = 0
    active = 0
    expired = 0

    with open(FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row: continue
            total += 1
            try:
                exp_date = datetime.date.fromisoformat(row[2])
                if exp_date >= today:
                    active += 1
                else:
                    expired += 1
            except Exception:
                active += 1

    # Write summary report to report.txt
    with open(REPORT_FILE, "w", encoding="utf-8") as rf:
        rf.write("========== SUMMARY REPORT ==========\n")
        rf.write(f"Total passes : {total}\n")
        rf.write(f"Active       : {active}\n")
        rf.write(f"Expired      : {expired}\n")
        rf.write("Report saved to report.txt\n")

    return total, active, expired

# Main Console Loop
def main():
    check_file()
    print("========== BUS PASS MENU ==========")
    print("  1. Register Passenger")
    print("  2. Issue Bus Pass")
    print("  3. Renew Pass")
    print("  4. Validate Pass")
    print("  5. View Summary Report")
    print("  6. Exit")
    print("====================================")

    while True:
        try:
            choice = input("Enter choice: ").strip()
            if not choice:
                continue
            choice_num = int(choice)
        except ValueError:
            print("Invalid input. Enter a number from 1 to 6.")
            continue

        if choice_num == 1:
            name = input("Name: ")
            age = input("Age: ")
            pid, bp_id = register_passenger(name, age)
            print(f"Passenger ID : {pid}")
            print("Record saved to passes.csv")

        elif choice_num == 2:
            pid = input("Passenger ID : ")
            name = input("Passenger Name: ")
            bp_id = issue_bus_pass(pid, name)
            print(f"Pass issued successfully. Pass ID: {bp_id}")
            print("Record saved to passes.csv")

        elif choice_num == 3:
            bp_id = input("Pass ID to renew: ")
            months = int(input("Enter renewal duration in months (e.g. 1, 3, 6): "))
            ok, new_exp = renew_pass(bp_id, months)
            if ok:
                print(f"Pass renewed successfully. New Expiry: {new_exp}")
                print("Record saved to passes.csv")
            else:
                print("Pass ID not found.")

        elif choice_num == 4:
            bp_id = input("Enter Pass ID: ")
            ok, status, exp = validate_pass(bp_id)
            if ok:
                print(f"Pass ID: {bp_id.upper()}   Status: {status}   (expires {exp})")
            else:
                print(f"Pass ID: {bp_id} not found.")

        elif choice_num == 5:
            total, active, expired = view_summary_report()
            print("========== SUMMARY REPORT ==========")
            print(f"Total passes : {total}")
            print(f"Active       : {active}")
            print(f"Expired      : {expired}")
            print("Report saved to report.txt")

        elif choice_num == 6:
            print("Records saved. Program closed.")
            break
        else:
            print("Invalid input. Enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
