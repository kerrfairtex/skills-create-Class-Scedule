To architect and deploy the **Class Schedule Management System** as a production-ready web application for the BSIT department at Tawi-Tawi Regional Agricultural College (TRAC), we must transition from manual, error-prone spreadsheets to a structured, centralized Management Information System (MIS) [1-3]. This system is designed as a specialized administrative asset that replaces decentralized methodologies with an automated, modular framework [4-6].

### 1. High-Level System Architecture
The application is architected as a **web-based system** strictly optimized for **desktop and laptop web browsers**, specifically excluding mobile device support to maintain the integrity of complex scheduling interfaces like drag-and-drop timetables [7-9]. 

*   **Backend Environment:** We utilize **Python 3.10+** for the core logic, as it is stable, mature, and directly relevant to the BSIT curriculum [10-12]. 
*   **Database Layer:** **SQLite 3** serves as the embedded, file-based relational database engine [10, 13, 14]. Its serverless nature is ideal for localized deployment, eliminating the need for complex server installations or professional administrative oversight [15-17].
*   **Deployment Model:** To ensure **100% operational availability** regardless of regional internet instability, the system is deployed on a centralized machine within a **Local Area Network (LAN)** [18-20].

### 2. Core Functional Modules (MOD-01 to MOD-08)
The system is decomposed into eight specialized modules to manage the scheduling lifecycle [21-23]:

*   **MOD-01 (Authentication):** Implements **Role-Based Access Control (RBAC)** for Admin, Faculty, and Students [24-26].
*   **MOD-02 (Master List Management):** The central repository for **CRUD operations** on teacher profiles (availability/subjects), curriculum data (subject codes/units), facility data (room capacities), and section information [23, 27-32].
*   **MOD-03 (Schedule Generation):** An algorithmic engine that automatically correlates instructors, rooms, and subjects with time slots based on pre-encoded constraints [21, 33, 34].
*   **MOD-04 (Conflict Detection):** A rigorous mathematical validation module achieving **100% accuracy** in identifying overlapping time slots, double-booked rooms, and teacher assignment conflicts [35-38].
*   **MOD-05 (Manual Adjustment):** Provides a visually intuitive **drag-and-drop interface** for administrators to fine-tune entries that the algorithm cannot satisfy for special edge cases [36, 39, 40].
*   **MOD-06 & MOD-07 (Stakeholder Access):** Tailored viewing and printing functionalities that generate role-specific timetables and formatted hardcopies [41-43].
*   **MOD-08 (Database Management):** A silent background service ensuring **relational integrity** and automated synchronization across all modules to prevent "orphaned" records [21, 44-46].

### 3. Data Integrity and Security Protocols
Production-grade deployment requires strict adherence to relational rules to maintain institutional data health [9, 47, 48].
*   **Relational Integrity:** Any modification in the master list—such as changing a teacher's availability—is automatically reflected across the entire system to prevent inconsistent scheduling [46, 49, 50].
*   **Bounded Scope:** To prevent **"feature creep"** and preserve high-performance speed, the system explicitly excludes auxiliary features such as grade computation, attendance tracking, and online enrollment [51-53].
*   **Data Persistence:** Regular backups are managed through the background service of MOD-08 to safeguard against data loss [54-56].

### 4. Infrastructure and Deployment Benchmarks
The hosting hardware must be robust enough to process high volumes of heterogeneous scheduling variables [2, 57, 58].
*   **Hardware Minimums:** An **Intel Core i3 processor** with **4GB of RAM** and **500MB of storage** is the baseline for stable performance [20, 59, 60].
*   **Critical Protection:** An **Uninterruptible Power Supply (UPS)** with an **Automatic Voltage Regulator (AVR)** is strictly required to protect the SQLite database from power fluctuations during transactions [54, 56, 61, 62].
*   **Phased Rollout:** Implementation begins exclusively in the BSIT department to refine data before expanding to other academic units [38, 56, 63].

This architectural framework ensures the college transitions into a streamlined, high-performance institutional asset that reduces the time for timetable creation by **60%** and administrative workloads by **40%** [64-66].