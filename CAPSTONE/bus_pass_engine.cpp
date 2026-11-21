#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <iomanip>
#include <ctime>
#include <algorithm>
#include <memory>
#include <map>

// ============================================================================
// BUS PASS AUTOMATION SYSTEM - C++ OOP CORE ENGINE
// Course: Object-Oriented Programming with C++
// Students: YOKAVISHWA A (192471017), ELAMARAN S (192524246), PUNITH KUMAR N (192525156)
// Guide: Mr Jegadeesh K | Saveetha Institute of Medical and Technical Sciences
// ============================================================================

namespace BusPassCore {

    // Utility: Trim strings
    inline std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(" \t\r\n");
        if (first == std::string::npos) return "";
        size_t last = str.find_last_not_of(" \t\r\n");
        return str.substr(first, (last - first + 1));
    }

    // Utility: Date structure and operations
    struct Date {
        int year;
        int month;
        int day;

        static Date today() {
            std::time_t t = std::time(nullptr);
            std::tm* now = std::localtime(&t);
            return { now->tm_year + 1900, now->tm_mon + 1, now->tm_mday };
        }

        static Date fromString(const std::string& s) {
            Date d{2026, 1, 1};
            if (s.empty()) return d;
            std::stringstream ss(s);
            char dash1, dash2;
            if (ss >> d.year >> dash1 >> d.month >> dash2 >> d.day) {
                return d;
            }
            return d;
        }

        std::string toString() const {
            std::ostringstream oss;
            oss << std::setfill('0') << std::setw(4) << year << "-"
                << std::setw(2) << month << "-"
                << std::setw(2) << day;
            return oss.str();
        }

        long toDays() const {
            int y = year, m = month, d = day;
            if (m < 3) {
                y--;
                m += 12;
            }
            return 365L * y + y / 4 - y / 100 + y / 400 + (153 * m - 457) / 5 + d - 306;
        }

        bool isBefore(const Date& other) const {
            return toDays() < other.toDays();
        }

        bool isAfter(const Date& other) const {
            return toDays() > other.toDays();
        }

        int daysBetween(const Date& other) const {
            return static_cast<int>(toDays() - other.toDays());
        }

        Date addDays(int days) const {
            long currentDays = toDays() + days;
            // Approximate calendar recovery
            long l = currentDays + 68569 + 2442113;
            long n = (4 * l) / 146097;
            l = l - (146097 * n + 3) / 4;
            long i = (4000 * (l + 1)) / 1461001;
            l = l - (1461 * i) / 4 + 31;
            long j = (80 * l) / 2447;
            int d = static_cast<int>(l - (2447 * j) / 80);
            l = j / 11;
            int m = static_cast<int>(j + 2 - (12 * l));
            int y = static_cast<int>(100 * (n - 49) + i + l);
            return { y, m, d };
        }

        Date addMonths(int months) const {
            return addDays(months * 30);
        }
    };

    // ========================================================================
    // PASSENGER CLASS (OOP Encapsulation)
    // ========================================================================
    class Passenger {
    private:
        std::string passengerId;
        std::string name;
        int age;
        std::string category; // Student, Regular, Senior

    public:
        Passenger() : passengerId(""), name(""), age(0), category("Regular") {}
        Passenger(const std::string& id, const std::string& n, int a, const std::string& cat = "Regular")
            : passengerId(id), name(n), age(a), category(cat) {}

        std::string getId() const { return passengerId; }
        std::string getName() const { return name; }
        int getAge() const { return age; }
        std::string getCategory() const { return category; }

        void setCategory(const std::string& cat) { category = cat; }
    };

    // ========================================================================
    // BUS PASS BASE CLASS (OOP Abstraction & Polymorphism)
    // ========================================================================
    class BusPass {
    protected:
        std::string passId;
        std::string passengerId;
        std::string passengerName;
        std::string routeFrom;
        std::string routeTo;
        Date issueDate;
        Date expiryDate;
        std::string passType; // Monthly, Quarterly, Annual
        double baseFare;

    public:
        BusPass(const std::string& pId, const std::string& pPassId, const std::string& pName,
                const std::string& from, const std::string& to,
                const Date& issue, const Date& expiry,
                const std::string& type, double fare)
            : passId(pId), passengerId(pPassId), passengerName(pName),
              routeFrom(from), routeTo(to), issueDate(issue), expiryDate(expiry),
              passType(type), baseFare(fare) {}

        virtual ~BusPass() = default;

        // Virtual methods demonstrating Polymorphism
        virtual double calculateFare() const = 0;
        virtual std::string getCategoryName() const = 0;

        std::string getPassId() const { return passId; }
        std::string getPassengerId() const { return passengerId; }
        std::string getPassengerName() const { return passengerName; }
        std::string getRouteFrom() const { return routeFrom; }
        std::string getRouteTo() const { return routeTo; }
        Date getIssueDate() const { return issueDate; }
        Date getExpiryDate() const { return expiryDate; }
        std::string getPassType() const { return passType; }

        void setExpiryDate(const Date& newExp) { expiryDate = newExp; }

        // Algorithm 2: Expiry Validation Algorithm
        std::string checkStatus(const Date& referenceDate = Date::today()) const {
            if (expiryDate.isBefore(referenceDate)) {
                return "EXPIRED";
            }
            int diff = expiryDate.daysBetween(referenceDate);
            if (diff <= 7) {
                return "EXPIRING_SOON";
            }
            return "VALID";
        }

        int getRemainingDays(const Date& referenceDate = Date::today()) const {
            return expiryDate.daysBetween(referenceDate);
        }

        virtual std::string toCSVRow() const {
            std::ostringstream oss;
            oss << passId << "," << passengerName << "," << expiryDate.toString() << ","
                << passengerId << "," << routeFrom << "," << routeTo << ","
                << issueDate.toString() << "," << passType << "," << getCategoryName() << ","
                << std::fixed << std::setprecision(2) << calculateFare();
            return oss.str();
        }

        virtual void toJSON(std::ostream& os) const {
            Date now = Date::today();
            os << "{"
               << "\"pass_id\":\"" << passId << "\","
               << "\"passenger_id\":\"" << passengerId << "\","
               << "\"name\":\"" << passengerName << "\","
               << "\"route_from\":\"" << routeFrom << "\","
               << "\"route_to\":\"" << routeTo << "\","
               << "\"issue_date\":\"" << issueDate.toString() << "\","
               << "\"expiry_date\":\"" << expiryDate.toString() << "\","
               << "\"pass_type\":\"" << passType << "\","
               << "\"category\":\"" << getCategoryName() << "\","
               << "\"fare\":" << calculateFare() << ","
               << "\"status\":\"" << checkStatus(now) << "\","
               << "\"days_remaining\":" << getRemainingDays(now)
               << "}";
        }
    };

    // ========================================================================
    // DERIVED CLASS 1: StudentPass (Concession Fare Algorithm)
    // ========================================================================
    class StudentPass : public BusPass {
    private:
        std::string institution;

    public:
        StudentPass(const std::string& pId, const std::string& pPassId, const std::string& pName,
                    const std::string& from, const std::string& to,
                    const Date& issue, const Date& expiry,
                    const std::string& type, double fare, const std::string& inst = "SIMATS")
            : BusPass(pId, pPassId, pName, from, to, issue, expiry, type, fare), institution(inst) {}

        double calculateFare() const override {
            // 70% Concession for students
            return baseFare * 0.30;
        }

        std::string getCategoryName() const override {
            return "Student";
        }
    };

    // ========================================================================
    // DERIVED CLASS 2: CommuterPass (Standard Regular Fare)
    // ========================================================================
    class CommuterPass : public BusPass {
    public:
        CommuterPass(const std::string& pId, const std::string& pPassId, const std::string& pName,
                     const std::string& from, const std::string& to,
                     const Date& issue, const Date& expiry,
                     const std::string& type, double fare)
            : BusPass(pId, pPassId, pName, from, to, issue, expiry, type, fare) {}

        double calculateFare() const override {
            // Standard fare
            return baseFare;
        }

        std::string getCategoryName() const override {
            return "General Commuter";
        }
    };

    // ========================================================================
    // DERIVED CLASS 3: SeniorCitizenPass (50% Concession)
    // ========================================================================
    class SeniorCitizenPass : public BusPass {
    public:
        SeniorCitizenPass(const std::string& pId, const std::string& pPassId, const std::string& pName,
                          const std::string& from, const std::string& to,
                          const Date& issue, const Date& expiry,
                          const std::string& type, double fare)
            : BusPass(pId, pPassId, pName, from, to, issue, expiry, type, fare) {}

        double calculateFare() const override {
            // 50% Concession for seniors
            return baseFare * 0.50;
        }

        std::string getCategoryName() const override {
            return "Senior Citizen";
        }
    };

    // ========================================================================
    // PASS MANAGER CLASS (Handles File I/O, Algorithms, Atomic Updates)
    // ========================================================================
    class PassManager {
    private:
        std::string csvFilePath;
        std::vector<std::shared_ptr<BusPass>> passes;

    public:
        explicit PassManager(const std::string& path = "passes.csv") : csvFilePath(path) {
            ensureFileExists();
            loadFromCSV();
        }

        // Module 3: Check and ensure file exists with header
        void ensureFileExists() {
            std::ifstream test(csvFilePath);
            if (!test.is_open()) {
                std::ofstream create(csvFilePath);
                if (create.is_open()) {
                    create << "pass_id,name,expiry,passenger_id,route_from,route_to,issue_date,pass_type,category,fare\n";
                    create.close();
                }
            }
        }

        // Module 2 Flow: Read passes.csv into memory
        void loadFromCSV() {
            passes.clear();
            std::ifstream file(csvFilePath);
            if (!file.is_open()) return;

            std::string line;
            bool header = true;
            while (std::getline(file, line)) {
                line = trim(line);
                if (line.empty()) continue;
                if (header) {
                    header = false;
                    continue; // skip header line
                }

                std::stringstream ss(line);
                std::string pId, name, expiryStr, passId, from, to, issueStr, type, cat, fareStr;
                std::getline(ss, pId, ',');
                std::getline(ss, name, ',');
                std::getline(ss, expiryStr, ',');

                // Check if extra fields exist, else provide defaults
                if (std::getline(ss, passId, ',')) {
                    std::getline(ss, from, ',');
                    std::getline(ss, to, ',');
                    std::getline(ss, issueStr, ',');
                    std::getline(ss, type, ',');
                    std::getline(ss, cat, ',');
                    std::getline(ss, fareStr, ',');
                } else {
                    passId = "P" + pId.substr(std::min<size_t>(2, pId.size()));
                    from = "Central Station";
                    to = "Campus / City";
                    issueStr = Date::today().toString();
                    type = "Monthly";
                    cat = "General Commuter";
                    fareStr = "500.00";
                }

                Date exp = Date::fromString(expiryStr);
                Date iss = Date::fromString(issueStr);
                double fare = 500.0;
                try {
                    if (!fareStr.empty()) fare = std::stod(fareStr);
                } catch (...) {
                    fare = 500.0;
                }

                std::shared_ptr<BusPass> ptr;
                if (cat == "Student") {
                    ptr = std::make_shared<StudentPass>(pId, passId, name, from, to, iss, exp, type, fare / 0.30);
                } else if (cat == "Senior Citizen") {
                    ptr = std::make_shared<SeniorCitizenPass>(pId, passId, name, from, to, iss, exp, type, fare / 0.50);
                } else {
                    ptr = std::make_shared<CommuterPass>(pId, passId, name, from, to, iss, exp, type, fare);
                }
                passes.push_back(ptr);
            }
            file.close();
        }

        // Module 2 Flow: Atomic rewrite using temporary file
        bool saveToCSV() {
            std::string tempPath = csvFilePath + ".tmp";
            std::ofstream temp(tempPath);
            if (!temp.is_open()) return false;

            temp << "pass_id,name,expiry,passenger_id,route_from,route_to,issue_date,pass_type,category,fare\n";
            for (const auto& pass : passes) {
                temp << pass->toCSVRow() << "\n";
            }
            temp.close();

            // Replace atomically
            std::remove(csvFilePath.c_str());
            return (std::rename(tempPath.c_str(), csvFilePath.c_str()) == 0);
        }

        // Algorithm 1: Next Pass ID and Passenger ID generation
        std::string generateNextPassId() {
            int maxId = 1000;
            for (const auto& p : passes) {
                std::string pid = p->getPassId();
                if (pid.length() > 2 && pid.substr(0, 2) == "BP") {
                    try {
                        int num = std::stoi(pid.substr(2));
                        if (num > maxId) maxId = num;
                    } catch (...) {}
                }
            }
            return "BP" + std::to_string(maxId + 1);
        }

        std::string generateNextPassengerId() {
            int maxId = 100;
            for (const auto& p : passes) {
                std::string pid = p->getPassengerId();
                if (pid.length() > 1 && pid[0] == 'P') {
                    try {
                        int num = std::stoi(pid.substr(1));
                        if (num > maxId) maxId = num;
                    } catch (...) {}
                }
            }
            return "P" + std::to_string(maxId + 1);
        }

        // Module 1: Issue Bus Pass
        std::shared_ptr<BusPass> issuePass(const std::string& name, int age,
                                          const std::string& from, const std::string& to,
                                          const std::string& passType, int durationMonths,
                                          const std::string& customCategory = "") {
            std::string passId = generateNextPassId();
            std::string passengerId = generateNextPassengerId();
            Date issueDate = Date::today();
            Date expiryDate = issueDate.addMonths(durationMonths > 0 ? durationMonths : 1);

            std::string category = customCategory;
            if (category.empty()) {
                if (age >= 60) category = "Senior Citizen";
                else if (age <= 24) category = "Student";
                else category = "General Commuter";
            }

            double baseMonthlyFare = 500.0;
            double baseFare = baseMonthlyFare * (durationMonths > 0 ? durationMonths : 1);

            std::shared_ptr<BusPass> newPass;
            if (category == "Student") {
                newPass = std::make_shared<StudentPass>(passId, passengerId, name, from, to, issueDate, expiryDate, passType, baseFare);
            } else if (category == "Senior Citizen") {
                newPass = std::make_shared<SeniorCitizenPass>(passId, passengerId, name, from, to, issueDate, expiryDate, passType, baseFare);
            } else {
                newPass = std::make_shared<CommuterPass>(passId, passengerId, name, from, to, issueDate, expiryDate, passType, baseFare);
            }

            passes.push_back(newPass);
            saveToCSV();
            return newPass;
        }

        // Algorithm 4: Search Pass by ID
        std::shared_ptr<BusPass> findPassById(const std::string& id) const {
            std::string target = trim(id);
            for (const auto& p : passes) {
                if (p->getPassId() == target || p->getPassengerId() == target) {
                    return p;
                }
            }
            return nullptr;
        }

        // Algorithm 3: Pass Renewal Algorithm
        bool renewPass(const std::string& passId, int additionalMonths, Date& newExpiryOut) {
            auto pass = findPassById(passId);
            if (!pass) return false;

            Date currentExp = pass->getExpiryDate();
            Date today = Date::today();
            // If already expired, renewal starts from today; if still valid, extend from current expiry
            Date base = currentExp.isBefore(today) ? today : currentExp;
            Date newExp = base.addMonths(additionalMonths > 0 ? additionalMonths : 1);

            pass->setExpiryDate(newExp);
            newExpiryOut = newExp;
            return saveToCSV();
        }

        // Algorithm 5: Summary Report & Analytics
        struct SummaryStats {
            int total;
            int active;
            int expired;
            int expiringSoon;
            double totalRevenue;
        };

        SummaryStats getSummary(const Date& refDate = Date::today()) const {
            SummaryStats stats{0, 0, 0, 0, 0.0};
            stats.total = static_cast<int>(passes.size());
            for (const auto& p : passes) {
                std::string st = p->checkStatus(refDate);
                if (st == "EXPIRED") {
                    stats.expired++;
                } else {
                    stats.active++;
                    if (st == "EXPIRING_SOON") {
                        stats.expiringSoon++;
                    }
                }
                stats.totalRevenue += p->calculateFare();
            }
            return stats;
        }

        // Module 2: Write summary report to report.txt
        bool writeSummaryReport(const std::string& reportPath = "report.txt") const {
            std::ofstream out(reportPath);
            if (!out.is_open()) return false;

            SummaryStats s = getSummary();
            out << "==========================================\n";
            out << "   BUS PASS AUTOMATION SYSTEM - REPORT    \n";
            out << "==========================================\n";
            out << "Generated Date: " << Date::today().toString() << "\n\n";
            out << "Total passes   : " << s.total << "\n";
            out << "Active         : " << s.active << "\n";
            out << "Expired        : " << s.expired << "\n";
            out << "Expiring Soon  : " << s.expiringSoon << "\n";
            out << "Total Revenue  : Rs. " << std::fixed << std::setprecision(2) << s.totalRevenue << "\n";
            out << "------------------------------------------\n";
            out << "Status: Report synchronized with passes.csv\n";
            out << "==========================================\n";
            out.close();
            return true;
        }

        const std::vector<std::shared_ptr<BusPass>>& getAllPasses() const {
            return passes;
        }
    };

} // namespace BusPassCore

// ============================================================================
// CLI INTERACTION DISPATCHER (JSON Bridge & Terminal Menu)
// ============================================================================
int main(int argc, char* argv[]) {
    BusPassCore::PassManager manager("passes.csv");

    if (argc > 1) {
        std::string cmd = argv[1];

        // 1. JSON List
        if (cmd == "--json-list") {
            std::cout << "[";
            const auto& all = manager.getAllPasses();
            for (size_t i = 0; i < all.size(); ++i) {
                all[i]->toJSON(std::cout);
                if (i + 1 < all.size()) std::cout << ",";
            }
            std::cout << "]" << std::endl;
            return 0;
        }

        // 2. Validate
        if (cmd == "--validate" && argc > 2) {
            std::string passId = argv[2];
            auto pass = manager.findPassById(passId);
            if (pass) {
                std::cout << "{\"found\":true,\"status\":\"" << pass->checkStatus() << "\","
                          << "\"pass_id\":\"" << pass->getPassId() << "\","
                          << "\"name\":\"" << pass->getPassengerName() << "\","
                          << "\"expiry\":\"" << pass->getExpiryDate().toString() << "\","
                          << "\"days_remaining\":" << pass->getRemainingDays() << "}" << std::endl;
            } else {
                std::cout << "{\"found\":false,\"error\":\"Pass not found\"}" << std::endl;
            }
            return 0;
        }

        // 3. Issue
        // Usage: --issue <name> <age> <from> <to> <type> <months> [category]
        if (cmd == "--issue" && argc >= 8) {
            std::string name = argv[2];
            int age = std::stoi(argv[3]);
            std::string from = argv[4];
            std::string to = argv[5];
            std::string type = argv[6];
            int months = std::stoi(argv[7]);
            std::string cat = (argc >= 9) ? argv[8] : "";

            auto p = manager.issuePass(name, age, from, to, type, months, cat);
            manager.writeSummaryReport();
            std::cout << "{\"success\":true,\"pass_id\":\"" << p->getPassId() << "\","
                      << "\"passenger_id\":\"" << p->getPassengerId() << "\","
                      << "\"name\":\"" << p->getPassengerName() << "\","
                      << "\"expiry\":\"" << p->getExpiryDate().toString() << "\","
                      << "\"fare\":" << p->calculateFare() << "}" << std::endl;
            return 0;
        }

        // 4. Renew
        // Usage: --renew <pass_id> <months>
        if (cmd == "--renew" && argc >= 4) {
            std::string passId = argv[2];
            int months = std::stoi(argv[3]);
            BusPassCore::Date newExp{2026, 1, 1};
            bool ok = manager.renewPass(passId, months, newExp);
            manager.writeSummaryReport();
            if (ok) {
                std::cout << "{\"success\":true,\"pass_id\":\"" << passId << "\","
                          << "\"new_expiry\":\"" << newExp.toString() << "\"}" << std::endl;
            } else {
                std::cout << "{\"success\":false,\"error\":\"Pass not found or could not renew\"}" << std::endl;
            }
            return 0;
        }

        // 5. Summary Report
        if (cmd == "--report") {
            auto s = manager.getSummary();
            manager.writeSummaryReport();
            std::cout << "{\"total\":" << s.total << ",\"active\":" << s.active
                      << ",\"expired\":" << s.expired << ",\"expiring_soon\":" << s.expiringSoon
                      << ",\"revenue\":" << s.totalRevenue << "}" << std::endl;
            return 0;
        }
    }

    // Interactive Console Menu Matching Slides 6, 8, 10
    std::cout << "========== BUS PASS MENU ==========\n";
    std::cout << " 1. Register Passenger\n";
    std::cout << " 2. Issue Bus Pass\n";
    std::cout << " 3. Renew Pass\n";
    std::cout << " 4. Validate Pass\n";
    std::cout << " 5. View Summary Report\n";
    std::cout << " 6. Exit\n";
    std::cout << "====================================\n";

    int choice = 0;
    while (true) {
        std::cout << "Enter choice: ";
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::string discard;
            std::cin >> discard;
            std::cout << "Invalid input. Enter a number from 1 to 6.\n";
            continue;
        }

        if (choice == 1) {
            std::string name;
            int age;
            std::cout << "Name: ";
            std::cin >> std::ws;
            std::getline(std::cin, name);
            std::cout << "Age: ";
            std::cin >> age;
            auto p = manager.issuePass(name, age, "Central Bus Stand", "Gandhipuram", "Monthly", 1);
            std::cout << "Passenger ID : " << p->getPassengerId() << "\n";
            std::cout << "Record saved to passes.csv\n";
        } else if (choice == 2) {
            std::string name;
            int age;
            std::cout << "Passenger ID : ";
            std::string pid;
            std::cin >> pid;
            std::cout << "Passenger Name: ";
            std::cin >> std::ws;
            std::getline(std::cin, name);
            auto p = manager.issuePass(name, 21, "Gandhipuram", "Saveetha Campus", "Monthly", 3, "Student");
            std::cout << "Pass issued successfully. Pass ID: " << p->getPassId() << "\n";
            std::cout << "Record saved to passes.csv\n";
        } else if (choice == 3) {
            std::string pid;
            int months;
            std::cout << "Pass ID to renew: ";
            std::cin >> pid;
            std::cout << "Enter renewal duration (months): ";
            std::cin >> months;
            BusPassCore::Date newExp{2026, 1, 1};
            if (manager.renewPass(pid, months, newExp)) {
                std::cout << "Pass renewed successfully until: " << newExp.toString() << "\n";
            } else {
                std::cout << "Pass ID not found.\n";
            }
        } else if (choice == 4) {
            std::string pid;
            std::cout << "Enter Pass ID: ";
            std::cin >> pid;
            auto pass = manager.findPassById(pid);
            if (pass) {
                std::cout << "Pass ID: " << pass->getPassId()
                          << "   Status: " << pass->checkStatus()
                          << "   (expires " << pass->getExpiryDate().toString() << ")\n";
            } else {
                std::cout << "Pass ID: " << pid << " not found.\n";
            }
        } else if (choice == 5) {
            auto s = manager.getSummary();
            manager.writeSummaryReport();
            std::cout << "========== SUMMARY REPORT ==========\n";
            std::cout << "Total passes : " << s.total << "\n";
            std::cout << "Active       : " << s.active << "\n";
            std::cout << "Expired      : " << s.expired << "\n";
            std::cout << "Report saved to report.txt\n";
        } else if (choice == 6) {
            std::cout << "Records saved. Program closed.\n";
            break;
        } else {
            std::cout << "Invalid input. Enter a number from 1 to 6.\n";
        }
    }

    return 0;
}
