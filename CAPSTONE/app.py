import streamlit as st
import pandas as pd
import datetime
import os
import json

# Local module imports
import cpp_bridge
import database

# ============================================================================
# BUS PASS AUTOMATION SYSTEM - STREAMLIT FRONTEND
# Course: Object-Oriented Programming with C++
// Team: YOKAVISHWA A (192471017), ELAMARAN S (192524246), PUNITH KUMAR N (192525156)
// Guide: Mr Jegadeesh K | Saveetha Institute of Medical and Technical Sciences
# ============================================================================

st.set_page_config(
    page_title="Bus Pass Automation System | C++ OOP Project",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# CUSTOM CSS: STRICT WHITE BACKGROUND, BLACK FONT, HIGH VISIBILITY DROPDOWNS
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background and Typography */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }

    /* Force all text elements to pure black */
    p, span, label, h1, h2, h3, h4, h5, h6, li, div {
        color: #000000 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 2px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Input Fields (Text, Number, Date) */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #333333 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #0066CC !important;
        box-shadow: 0 0 0 1px #0066CC !important;
    }

    /* HIGH-CONTRAST DROPDOWN / SELECTBOX STYLING */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    /* Dropdown Options Popup Menu */
    ul[data-baseweb="menu"], div[data-baseweb="popover"], div[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-bottom: 1px solid #E5E7EB !important;
        padding: 10px 14px !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #0066CC !important;
        color: #FFFFFF !important;
        border: 2px solid #0052A3 !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #0052A3 !important;
        border-color: #003D7A !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }
    .stButton > button * {
        color: #FFFFFF !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        padding: 14px !important;
    }
    div[data-testid="stMetricLabel"] * {
        color: #374151 !important;
        font-weight: bold !important;
    }
    div[data-testid="stMetricValue"] * {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Tab navigation */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 2px solid #000000 !important;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6 !important;
        border: 1px solid #D1D5DB !important;
        border-bottom: none !important;
        border-radius: 6px 6px 0 0 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066CC !important;
        color: #FFFFFF !important;
        border-color: #0066CC !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
    }

    /* Digital Bus Pass Card */
    .bus-pass-card {
        background-color: #FFFFFF;
        border: 3px solid #000000;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 6px 6px 0px #000000;
        margin: 15px 0;
        position: relative;
    }
    .badge-valid {
        background-color: #D1FAE5;
        color: #065F46 !important;
        border: 2px solid #059669;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-expired {
        background-color: #FEE2E2;
        color: #991B1B !important;
        border: 2px solid #DC2626;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-expiring {
        background-color: #FEF3C7;
        color: #92400E !important;
        border: 2px solid #D97706;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Code/Terminal Box */
    .terminal-box {
        background-color: #1E1E1E !important;
        color: #39FF14 !important;
        font-family: 'Consolas', monospace;
        padding: 16px;
        border-radius: 8px;
        border: 2px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HEADER & PROJECT CREDITS
# ----------------------------------------------------------------------------
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown("<h1 style='margin-bottom: 0px;'>🚌 Bus Pass Automation System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #4B5563 !important; margin-top: 4px;'>Menu-Driven Architecture with File Handling & C++ OOP Core Engine</h4>", unsafe_allow_html=True)

with col_head2:
    is_compiled, comp_msg = cpp_bridge.compile_cpp_if_needed()
    if cpp_bridge.has_cpp_binary():
        st.success("⚡ C++ Engine: Active (`.exe`)")
    else:
        st.info("🔄 C++ Engine: Python Bridge")

st.markdown("""
<div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 10px 16px; margin-bottom: 20px;">
    <b>Team Members:</b> YOKAVISHWA A (192471017) | ELAMARAN S (192524246) | PUNITH KUMAR N (192525156)<br>
    <b>Guided by:</b> Mr Jegadeesh K (Industrial Professional, Coimbatore) | <b>Institution:</b> Saveetha Institute of Medical and Technical Sciences
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TOP METRICS DASHBOARD (C++ Summary Statistics Algorithm)
# ----------------------------------------------------------------------------
summary_data = cpp_bridge.cpp_get_summary()

m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
with m_col1:
    st.metric("Total Passes", summary_data["total"])
with m_col2:
    st.metric("Active Passes", summary_data["active"])
with m_col3:
    st.metric("Expired Passes", summary_data["expired"])
with m_col4:
    st.metric("Expiring Soon", summary_data.get("expiring_soon", 0))
with m_col5:
    st.metric("Total Revenue", f"₹ {summary_data['revenue']:,.2f}")

st.markdown("<hr style='border: 1px solid #E5E7EB; margin: 15px 0;'>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# MAIN INTERFACE TABS
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📝 1. Register & Issue Pass",
    "🔄 2. Renew Pass",
    "🔍 3. Validate Pass",
    "📊 4. Summary & Reports",
    "🗄️ 5. Database & CSV Sync",
    "⚙️ 6. C++ OOP Architecture",
    "💻 7. Console Simulator"
])

# ============================================================================
# TAB 1: PASSENGER REGISTRATION & PASS ISSUANCE (Module 1)
# ============================================================================
with tab1:
    st.subheader("Module 1: Passenger Registration & Pass Issuance")
    st.caption("Replaces manual paper registers with auto-generated Pass ID and instant file persistence (passes.csv & SQLite).")

    with st.form("issue_pass_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Passenger Full Name *", placeholder="e.g. Yokavishwa A")
            age = st.number_input("Age *", min_value=5, max_value=100, value=21, step=1)
            contact = st.text_input("Contact Number", placeholder="e.g. 9876543210")
            category_choice = st.selectbox(
                "Passenger Category *",
                ["Student (70% Concession)", "General Commuter (Standard)", "Senior Citizen (50% Concession)"]
            )

        with c2:
            route_from = st.selectbox(
                "Source Station / Stop *",
                ["Central Bus Stand", "Gandhipuram", "Singanallur", "Ukkadam", "Peelamedu", "Railway Junction", "RS Puram"]
            )
            route_to = st.selectbox(
                "Destination / Campus *",
                ["Saveetha Campus", "CIT / Peelamedu", "PSG Tech", "Town Hall", "Saravanampatti", "Hope College"]
            )
            pass_type = st.selectbox("Pass Type *", ["Monthly (1 Month)", "Quarterly (3 Months)", "Annual (12 Months)"])
            
            duration_months = 1
            if "Quarterly" in pass_type: duration_months = 3
            elif "Annual" in pass_type: duration_months = 12

            # Real-time C++ Fare Calculation Algorithm Preview
            base_rate = 500.0 * duration_months
            if "Student" in category_choice:
                calc_fare = base_rate * 0.30
                cat_tag = "Student"
            elif "Senior" in category_choice:
                calc_fare = base_rate * 0.50
                cat_tag = "Senior Citizen"
            else:
                calc_fare = base_rate
                cat_tag = "General Commuter"

            st.markdown(f"""
            <div style="background-color: #F1F5F9; border: 2px dashed #0066CC; border-radius: 8px; padding: 12px; margin-top: 15px;">
                <span style="font-weight: bold; color: #000000;">Calculated Fare (C++ Fare Algorithm):</span>
                <span style="font-size: 22px; font-weight: 800; color: #0066CC; float: right;">₹ {calc_fare:.2f}</span>
            </div>
            """, unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Register Passenger & Issue Bus Pass")

        if submitted:
            if not name.strip():
                st.error("Please enter the passenger's name.")
            else:
                # Call C++ Engine
                result = cpp_bridge.cpp_issue_pass(
                    name=name.strip(),
                    age=age,
                    route_from=route_from,
                    route_to=route_to,
                    pass_type=pass_type.split()[0],
                    duration_months=duration_months,
                    category=cat_tag
                )
                
                # Also save to SQLite database
                database.db_insert_pass(
                    pass_id=result["pass_id"],
                    passenger_id=result["passenger_id"],
                    name=name.strip(),
                    age=age,
                    r_from=route_from,
                    r_to=route_to,
                    issue_date=str(datetime.date.today()),
                    expiry_date=result["expiry"],
                    pass_type=pass_type.split()[0],
                    category=cat_tag,
                    fare=result["fare"]
                )

                st.success(f"✅ Pass Issued Successfully! Engine Used: {result.get('engine', 'C++ Engine')}")

                # Display the issued card
                st.markdown(f"""
                <div class="bus-pass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000000; padding-bottom: 8px; margin-bottom: 12px;">
                        <div>
                            <span style="font-size: 20px; font-weight: bold; color: #000000;">🚌 TAMIL NADU STATE TRANSPORT - DIGITAL BUS PASS</span><br>
                            <span style="font-size: 13px; color: #4B5563;">Saveetha Institute Educational & Commuter Concession</span>
                        </div>
                        <span class="badge-valid">STATUS: VALID</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 15px;">
                        <div><b>Pass ID:</b> <span style="font-family: monospace; font-size: 18px; font-weight: bold;">{result['pass_id']}</span></div>
                        <div><b>Passenger ID:</b> <span style="font-family: monospace; font-size: 16px;">{result['passenger_id']}</span></div>
                        <div><b>Passenger Name:</b> {result['name']}</div>
                        <div><b>Category:</b> {cat_tag}</div>
                        <div><b>Route:</b> {route_from} ➔ {route_to}</div>
                        <div><b>Fare Paid:</b> ₹ {result['fare']:.2f}</div>
                        <div><b>Issue Date:</b> {datetime.date.today()}</div>
                        <div><b>Expiry Date:</b> <span style="font-weight: bold; color: #059669;">{result['expiry']}</span></div>
                    </div>
                    <div style="margin-top: 15px; font-size: 12px; color: #6B7280; border-top: 1px solid #E5E7EB; padding-top: 8px;">
                        Record safely appended to passes.csv and synchronized with SQLite bus_pass.db.
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: PASS RENEWAL (Module 2)
# ============================================================================
with tab2:
    st.subheader("Module 2: Pass Renewal")
    st.caption("Extends the validity of expiring or expired bus passes with automatic atomic file updates (Slide 8).")

    all_passes = cpp_bridge.cpp_get_all_passes()
    pass_options = [f"{p['pass_id']} - {p['name']} (Expires: {p['expiry_date']}) [{p['status']}]" for p in all_passes]

    col_r1, col_r2 = st.columns([3, 2])
    with col_r1:
        if pass_options:
            selected_pass_str = st.selectbox("Select Pass to Renew *", pass_options)
            selected_pass_id = selected_pass_str.split(" - ")[0]
        else:
            selected_pass_id = st.text_input("Enter Pass ID (e.g. BP1001)")

        renew_months = st.selectbox("Renewal Duration *", [1, 3, 6, 12], format_func=lambda m: f"{m} Month(s)")

        if st.button("🔄 Execute C++ Pass Renewal"):
            if not selected_pass_id:
                st.error("Please specify a Pass ID.")
            else:
                res = cpp_bridge.cpp_renew_pass(selected_pass_id, renew_months)
                if res.get("success"):
                    database.db_renew_pass(selected_pass_id, renew_months, res["new_expiry"])
                    st.success(f"🎉 Pass {selected_pass_id} renewed until {res['new_expiry']}!")
                    st.info(f"File flow complete: passes.csv.tmp written and replaced. Summary report updated.")
                else:
                    st.error(f"Error: {res.get('error', 'Could not renew pass.')}")

    with col_r2:
        st.markdown("""
        <div style="background-color: #F8FAFC; border: 2px solid #000000; border-radius: 8px; padding: 16px;">
            <h4 style="margin-top: 0; color: #000000;">Renewal Architecture (Slide 8)</h4>
            <ol style="margin-left: -15px; font-size: 14px; line-height: 1.6;">
                <li>Read <code>passes.csv</code> into memory.</li>
                <li>Check expiry date with <code>date.today()</code>.</li>
                <li>Extend date by N months from current date or today.</li>
                <li>Write updated rows to temporary file (<code>passes.csv.tmp</code>).</li>
                <li>Replace original using atomic file replace.</li>
                <li>Synchronize with <code>report.txt</code> and SQLite database.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: REAL-TIME PASS VALIDATION (Module 2)
# ============================================================================
with tab3:
    st.subheader("Module 2: Pass Validation")
    st.caption("Checks the pass expiry against today's date in real-time, matching Slide 8 & 9.")

    v_col1, v_col2 = st.columns([2, 3])
    with v_col1:
        val_input = st.text_input("Enter Pass ID to Validate *", value="BP1001", placeholder="BP1001 or P101")
        validate_btn = st.button("🔍 Check Pass Status")

    with v_col2:
        if validate_btn or val_input:
            v_res = cpp_bridge.cpp_validate_pass(val_input.strip())
            if v_res.get("found"):
                status = v_res["status"]
                expiry = v_res["expiry"]
                days = v_res.get("days_remaining", 0)

                if status == "VALID":
                    badge = f'<span class="badge-valid">STATUS: VALID ({days} days remaining)</span>'
                elif status == "EXPIRING_SOON":
                    badge = f'<span class="badge-expiring">STATUS: EXPIRING SOON ({days} days remaining)</span>'
                else:
                    badge = f'<span class="badge-expired">STATUS: EXPIRED (Passed by {abs(days)} days)</span>'

                st.markdown(f"""
                <div class="bus-pass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #000000; padding-bottom: 8px;">
                        <span style="font-size: 18px; font-weight: bold;">PASS VERIFICATION RESULT</span>
                        {badge}
                    </div>
                    <div style="margin-top: 12px; font-size: 16px;">
                        <b>Pass ID:</b> <span style="font-family: monospace; font-size: 18px;">{v_res['pass_id']}</span><br>
                        <b>Passenger Name:</b> {v_res['name']}<br>
                        <b>Expiry Date:</b> <span style="font-weight: bold;">{expiry}</span><br>
                        <b>Engine:</b> {v_res.get('engine', 'C++ Algorithm Engine')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ {v_res.get('error', 'Pass not found in records.')}")

# ============================================================================
# TAB 4: SUMMARY REPORT & ANALYTICS (Module 2)
# ============================================================================
with tab4:
    st.subheader("Module 2: Summary Report & Analytics")
    st.caption("Auto-generated summary report file (report.txt) and visual transport analytics.")

    rep_col1, rep_col2 = st.columns([1, 1])

    with rep_col1:
        st.markdown("#### Generated `report.txt` (Slide 9)")
        if os.path.exists("report.txt"):
            with open("report.txt", "r", encoding="utf-8") as rf:
                report_content = rf.read()
            st.code(report_content, language="text")
        else:
            st.info("Click below to generate report.txt")

        if st.button("📄 Re-generate & Sync report.txt"):
            cpp_bridge.cpp_get_summary()
            st.success("report.txt refreshed successfully!")
            st.rerun()

    with rep_col2:
        st.markdown("#### Pass Breakdown Analytics")
        all_p = cpp_bridge.cpp_get_all_passes()
        if all_p:
            df_passes = pd.DataFrame(all_p)
            status_counts = df_passes["status"].value_counts()
            st.bar_chart(status_counts)

            cat_counts = df_passes["category"].value_counts()
            st.markdown("<b>Passes by Category:</b>", unsafe_allow_html=True)
            st.dataframe(cat_counts, use_container_width=True)

# ============================================================================
# TAB 5: DATABASE & CSV LIVE EXPLORER
# ============================================================================
with tab5:
    st.subheader("Database & CSV File Synchronizer")
    st.caption("Live records in SQLite `bus_pass.db` and CSV storage `passes.csv`.")

    search_query = st.text_input("🔍 Search Passes (By ID, Name, or Route)", placeholder="Type to filter...")

    if search_query.strip():
        records = database.db_search_passes(search_query.strip())
    else:
        records = database.db_get_all_passes()

    if records:
        df_records = pd.DataFrame(records)
        st.dataframe(df_records, use_container_width=True, height=350)
    else:
        st.warning("No pass records found.")

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if os.path.exists("passes.csv"):
            with open("passes.csv", "rb") as f:
                st.download_button("📥 Download passes.csv", data=f, file_name="passes.csv", mime="text/csv")
    with exp_col2:
        if st.button("🔄 Force Re-sync SQLite with passes.csv"):
            database.sync_csv_from_db()
            st.success("Synchronized SQLite and passes.csv!")
            st.rerun()

# ============================================================================
# TAB 6: C++ OOP ARCHITECTURE & DIAGNOSTICS
# ============================================================================
with tab6:
    st.subheader("Object-Oriented Programming with C++ Core Architecture")
    st.markdown("""
    This project strictly fulfills the requirements of the **Object-Oriented Programming with C++** course syllabus:
    
    1. **Encapsulation & Data Hiding:**
       - Class `Passenger`: Private attributes for `passengerId`, `name`, `age`, `category` with public accessors and mutators.
    2. **Inheritance & Polymorphism:**
       - Abstract Base Class `BusPass`: Defines virtual functions `calculateFare()`, `getCategoryName()`, `toCSVRow()`, and `toJSON()`.
       - Derived Classes:
         * `StudentPass` overrides `calculateFare()` implementing a 70% student discount.
         * `CommuterPass` overrides `calculateFare()` with regular commuter fare.
         * `SeniorCitizenPass` overrides `calculateFare()` with a 50% discount for seniors.
    3. **File Handling & Atomic Operations:**
       - `PassManager`: Reads records from `passes.csv`, validates expiry, writes to a temporary file (`passes.csv.tmp`), and atomically replaces it using `std::rename` / `os.replace`.
    4. **Algorithms:**
       - **ID Generation:** Format `BP1001` and `P101` with sequential collision tracking.
       - **Date Validation:** Gregorian date comparison with `today()`, leap-year day offset calculations.
       - **Search & Sort:** Lookup by Pass ID and status-based counting.
    """)

    st.markdown("#### C++ Source Code (`bus_pass_engine.cpp`)")
    if os.path.exists("bus_pass_engine.cpp"):
        with open("bus_pass_engine.cpp", "r", encoding="utf-8") as cf:
            cpp_code = cf.read()
        with st.expander("Click to view full C++ source code"):
            st.code(cpp_code, language="cpp")

# ============================================================================
# TAB 7: CONSOLE MENU SIMULATOR (Slides 6, 8, 10 Emulation)
# ============================================================================
with tab7:
    st.subheader("Console Menu Simulator (Terminal Output Demonstration)")
    st.caption("Demonstrates the exact console outputs shown in Slide 6, 8, and 10 of the presentation.")

    st.markdown("""
    <div class="terminal-box">
        <span style="color: #FFD700;">========== BUS PASS MENU ==========</span><br>
        &nbsp;1. Register Passenger<br>
        &nbsp;2. Issue Bus Pass<br>
        &nbsp;3. Renew Pass<br>
        &nbsp;4. Validate Pass<br>
        &nbsp;5. View Summary Report<br>
        &nbsp;6. Exit<br>
        <span style="color: #FFD700;">====================================</span><br>
    </div>
    """, unsafe_allow_html=True)

    sim_choice = st.radio("Simulate Menu Option:", [
        "1. Register Passenger",
        "2. Issue Bus Pass",
        "3. Renew Pass",
        "4. Validate Pass",
        "5. View Summary Report"
    ], horizontal=True)

    if "1." in sim_choice:
        st.code("""
Enter choice: 1
Name: Yokavishwa A
Age: 21
Passenger ID : P101
Record saved to passes.csv
        """, language="text")

    elif "2." in sim_choice:
        st.code("""
Enter choice: 2
Passenger ID : P101
Pass issued successfully. Pass ID: BP1001
Record saved to passes.csv
        """, language="text")

    elif "3." in sim_choice:
        st.code("""
Enter choice: 3
Pass ID to renew: BP1001
Enter renewal duration in months (e.g. 1, 3, 6): 3
Pass renewed successfully until: 2027-06-30
Record saved to passes.csv
        """, language="text")

    elif "4." in sim_choice:
        st.code("""
Enter choice: 4
Pass ID: BP1001   Status: VALID   (expires 2027-03-31)
        """, language="text")

    elif "5." in sim_choice:
        st.code(f"""
Enter choice: 5
========== SUMMARY REPORT ==========
Total passes : {summary_data['total']}
Active       : {summary_data['active']}
Expired      : {summary_data['expired']}
Report saved to report.txt
        """, language="text")
