# J-INVESTMENTS Fleet Management System

![Version](https://img.shields.io/badge/version-1.0.3-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

A comprehensive diesel tracking and fleet management system built with Python Dash, featuring real-time monitoring, analytics, and role-based access control.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [User Roles](#-user-roles)
- [Features Guide](#-features-guide)
- [Data Import](#-data-import)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Security](#-security)
- [Support](#-support)

---

## ✨ Features

### Core Functionality
- 🚜 **Fleet Asset Management** - Track machines, models, fuel rates, and capacities
- 👷 **Operator Management** - Manage operators with badge numbers and assignments
- ⛽ **Refueling Logs** - Record and monitor fuel usage with automatic calculations
- 📊 **Analytics Dashboard** - Real-time insights with interactive charts and KPIs
- 🔍 **Anomaly Detection** - Automatic flagging of unusual fuel consumption patterns

### Enterprise Features
- 🔐 **Multi-User Authentication** - Secure login with session management
- 👥 **Role-Based Access Control (RBAC)** - 4 role levels (Admin, Manager, Data Entry, Viewer)
- 🔒 **Admin Password Protection** - Additional security for delete operations
- 📝 **Complete Audit Logging** - Track all system changes and user actions
- 💾 **Excel Import/Export** - Bulk data operations with validation
- 📦 **JSON Backup/Restore** - Complete system data backup
- 🎨 **CAT Yellow Branding** - Professional design with custom logo support

### Analytics & Reporting
- 📈 Expected vs Delivered Fuel Charts
- 🎯 Machine Performance Analysis
- 👤 Operator Efficiency Tracking
- 📊 Period Summary Statistics
- ⚠️ Anomaly Reports
- 📉 Fuel Consumption Trends

---

## 🛠 Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web server and session management
- **SQLite** - Embedded database

### Frontend
- **Dash** - Interactive web framework
- **Plotly** - Data visualization
- **Dash Bootstrap Components** - UI components
- **Font Awesome** - Icons

### Data Processing
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations
- **OpenPyXL** - Excel file handling

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# pip package manager
pip --version
```

### Step 1: Clone or Download

```bash
# Download and extract the project files
# Or use git if available:
git clone <repository-url>
cd j-investments-fleet
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
dash>=2.14.0
dash-bootstrap-components>=1.5.0
plotly>=5.17.0
pandas>=2.1.0
openpyxl>=3.1.0
```

### Step 3: Verify Assets

Ensure the following directory structure:

```
your-project/
├── app.py (or dash_app.py)
├── config.py
├── database.py
├── requirements.txt
├── assets/
│   ├── login_split.css
│   └── J-INVESTMENTS-LOGO.svg
└── j_investments_fleet.db (created automatically)
```

---

## 🚀 Quick Start

### 1. Run the Application

```bash
python app.py
```

**Expected output:**
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

### 2. Access the System

Open your browser and navigate to:
```
http://localhost:8050
```

### 3. Default Login

```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT:** Change the default password immediately after first login!

### 4. Change Password

1. Click on your user avatar (top right)
2. Select "Change Password"
3. Enter current password: `admin123`
4. Enter new password (minimum 8 characters)
5. Confirm new password

---

## 👥 User Roles

### Admin
**Full system access**
- ✅ All CRUD operations
- ✅ User management
- ✅ System settings
- ✅ Delete operations (with admin password)
- ✅ Audit log access
- ✅ Import/Export data

### Manager
**Operational management**
- ✅ All CRUD operations on fleet data
- ✅ View reports and analytics
- ✅ Delete records (with admin password)
- ❌ Cannot manage users
- ❌ Cannot modify system settings

### Data Entry
**Daily operations**
- ✅ Add/Edit machines, operators, refueling logs
- ✅ View analytics
- ❌ Cannot delete records
- ❌ Cannot manage users
- ❌ Cannot modify settings

### Viewer
**Read-only access**
- ✅ View all data
- ✅ View analytics
- ✅ Generate reports
- ❌ Cannot add/edit/delete
- ❌ Cannot manage users

---

## 📖 Features Guide

### Fleet Assets Management

**Add New Machine:**
1. Navigate to **Fleet Assets** tab
2. Fill in the form:
   - Machine ID (e.g., EX-001)
   - Model (e.g., CAT 320)
   - Fuel Rate (L/hr)
   - Tank Capacity (L)
3. Click **Add Machine**

**Edit Machine:**
- Click on any field in the table
- Modify the value
- Changes save automatically

**Delete Machine:**
- Click **Delete** button (Admin/Manager only)
- Enter admin password
- Confirm deletion

### Operator Management

**Add Operator:**
1. Go to **Operators** tab
2. Enter:
   - Badge Number (unique identifier)
   - Full Name
3. Click **Add Operator**

**View Active Operators:**
- See all registered operators in the table
- Badge numbers are unique and cannot be duplicated

### Refueling Operations

**Log Refueling:**
1. Navigate to **Refueling** tab
2. Select:
   - Machine from dropdown
   - Operator from dropdown
   - Hours worked
   - Fuel issued (liters)
3. Add optional notes
4. Click **Add Entry**

**View Logs:**
- **Today**: Shows today's entries only
- **This Week**: Shows last 7 days
- **All History**: Shows all records

**Understanding Variance:**
- Expected Fuel = Hours Worked × Machine Rate
- Variance = Actual Fuel - Expected Fuel
- ⚠️ **Anomaly**: Variance exceeds tolerance threshold (default 10%)

**Summary Statistics:**
Each refueling view shows:
- Total Entries
- Total Fuel Used
- Total Machine Hours
- Expected Fuel
- Anomalies Detected

### Analytics Dashboard

**Date Range Filter:**
1. Select "From" date
2. Select "To" date
3. Click **Apply**
4. Click **Reset** to return to last 30 days

**KPI Cards:**
- 📊 Used Fuel - Total fuel consumed in period
- 🎯 Expected Fuel - Calculated expected consumption
- ⏱️ Total Machine Hours - Sum of all usage hours
- ⚠️ Anomalies - Count of variance alerts

**Charts:**

1. **Expected vs Delivered Fuel**
   - Blue line: Expected fuel consumption
   - Yellow line: Actual fuel delivered
   - Helps identify trends and patterns

2. **Machine Performance**
   - Bar chart of total fuel by machine
   - Color-coded by efficiency:
     - Green: >95% efficiency
     - Yellow: 85-95% efficiency
     - Red: <85% efficiency

3. **Operator Performance Table**
   - Total fuel used per operator
   - Total hours worked
   - Efficiency percentage
   - Number of entries

---

## 📥 Data Import

### Excel Import

**Supported Format:**

Your Excel file must have these sheets:

**Sheet 1: "Operators"**
```
| Operator    | Badge Number |
|-------------|--------------|
| John Doe    | B001         |
| Jane Smith  | B002         |
```

**Sheet 2: "Assets"**
```
| Machine ID | Model     | Rate | Capacity |
|------------|-----------|------|----------|
| EX-001     | CAT 320   | 8    | 150      |
| EX-002     | EXCAVATOR | 17   | 200      |
```

**Sheet 3: "Refueling"**
```
| Time                | Machine | Operator  | Hours worked | Fuel issued |
|---------------------|---------|-----------|--------------|-------------|
| 2026-01-13 08:00:00 | EX-001  | John Doe  | 5.5          | 44.0        |
| 2026-01-13 10:00:00 | EX-002  | Jane Smith| 3.2          | 54.4        |
```

**Import Steps:**
1. Navigate to **Settings** tab
2. Click **Import Excel**
3. Select your Excel file
4. Wait for processing
5. Review import summary

**Import Features:**
- ✅ Automatic duplicate detection
- ✅ Data validation
- ✅ Error reporting
- ✅ Skips invalid entries
- ✅ Logs import to audit trail

**Sample Data:**
Use `sample_import_data.xlsx` to see the correct format.

---

## ⚙️ Configuration

### config.py Settings

**Color Scheme:**
```python
COLORS = {
    'cat_yellow': '#FFB400',      # Primary brand color
    'cat_yellow_dark': '#cc9000',  # Darker shade
    'carbon': '#1a1a1a',           # Dark cards
    'steel': '#2d2d2d',            # Medium gray
    'text_bright': '#f0f0f0',      # White text
    'text_dim': '#a0a0a0',         # Gray text
    'danger': '#ff4d4d',           # Red alerts
    'success': '#2ecc71',          # Green success
    'bg_dark': '#0a0a0a',          # Black background
}
```

**Change Application Port:**

In `app.py` (last line):
```python
app.run_server(debug=True, host='0.0.0.0', port=8050)
```

Change `8050` to your desired port.

---

## 🔧 Troubleshooting

### Common Issues

**1. Port Already in Use**

```bash
# Error: Address already in use
```

**Solution:**
```python
# In app.py, change the port
app.run_server(debug=True, port=8051)
```

**2. Module Not Found**

```bash
# Error: ModuleNotFoundError: No module named 'dash'
```

**Solution:**
```bash
pip install -r requirements.txt
```

**3. Database Locked**

```bash
# Error: database is locked
```

**Solution:**
- Close all instances of the application
- Delete `j_investments_fleet.db-journal` if it exists
- Restart the application

**4. Logo Not Displaying**

**Check:**
- File exists at `assets/J-INVESTMENTS-LOGO.svg`
- File permissions are readable
- Clear browser cache (Ctrl+F5)

**5. Excel Import Fails**

**Common causes:**
- Sheet names don't match exactly (case-sensitive)
- Column names are different
- Duplicate Machine IDs or Badge Numbers
- Invalid date formats

**Solution:**
Use `sample_import_data.xlsx` as a template.

---

## 🔒 Security

### Best Practices

**1. Change Default Credentials**
```
✅ DO: Change admin password immediately
❌ DON'T: Use admin123 in production
```

**2. Set Admin Password**
```
✅ DO: Set a strong admin password for deletes
❌ DON'T: Leave it unset or use weak passwords
```

**3. User Management**
```
✅ DO: Assign minimum required permissions
❌ DON'T: Give everyone admin access
```

**4. Regular Backups**
```
✅ DO: Export data regularly (weekly)
❌ DON'T: Rely solely on the database file
```

### Password Requirements

- Minimum 8 characters
- No maximum length
- Recommended: Use strong passwords with mixed characters

---

## 🆘 Support

### Getting Help

**Documentation:**
- `README.md` - This file
- `INSTALLATION.md` - Detailed setup guide
- `FIXES.md` - Bug fixes and updates

**Self-Service:**
1. Check Troubleshooting section above
2. Review error messages in terminal
3. Check browser console (F12)
4. Verify data format for imports

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 100MB free space
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+

### Recommended
- **RAM**: 4GB or more
- **Storage**: 500MB free space
- **Browser**: Latest Chrome or Firefox

---

## 🔄 Version History

- **v1.0.3** (2026-01-16): Analytics improvements, bug fixes
- **v1.0.2** (2026-01-16): Excel import feature added
- **v1.0.1** (2026-01-16): UI enhancements
- **v1.0.0** (2026-01-15): Initial release

---

## 📝 License

MIT License

Copyright (c) 2026 J-INVESTMENTS

---

**Last Updated:** January 16, 2026  
**Version:** 1.0.3  
**Status:** Production Ready ✅

---

Made with ❤️ by J-INVESTMENTS Team
