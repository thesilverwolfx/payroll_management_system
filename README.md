# Simple Payroll Management System

A minimal web-based payroll management system built with Flask.

## Features

- Add and remove employees
- Update hours worked for employees
- Calculate payroll for all employees
- Simple, clean web interface

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

- **Add Employee**: Enter name, employee ID, and hourly rate
- **Update Hours**: Enter employee ID and hours worked
- **View Payroll**: The payroll report shows automatically with all calculations
- **Remove Employee**: Click the remove button next to any employee

Data is automatically saved to `payroll_data.json`.


