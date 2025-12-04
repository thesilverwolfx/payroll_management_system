# Simple Payroll Management System

A minimal web-based payroll management system built with Flask.

## Features

- Add and remove employees with hourly rate, department, allowances, and deductions
- Update hours, allowances, and deductions for employees in one step
- Automatic overtime calculation (1.5× rate above 40 hours) with gross and net breakdowns
- Real-time payroll dashboard with totals, averages, and employee stats
- Downloadable CSV payroll report for use in spreadsheets or audits
- Simple, clean web interface backed by local JSON storage

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to:
```
http://localhost:5000
```

## Usage

- **Add Employee**: Enter name, employee ID, department (optional), hourly rate, allowances, and deductions
- **Update Compensation**: Enter employee ID and update hours, allowances, or deductions (leave a field blank to keep the current value)
- **View Payroll**: Review the payroll report for overtime, allowances, deductions, gross, and net pay along with a summary dashboard
- **Remove Employee**: Click the remove button next to any employee
- **Export Payroll**: Click “Download CSV Report” to export the latest payroll snapshot

Data is automatically saved to `payroll_data.json`.


