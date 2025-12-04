import csv
import io
import json
import os

class Employee:
    def __init__(self, name, employee_id, hourly_rate, hours_worked=0, department='', allowances=0, deductions=0):
        self.name = name
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        self.department = department
        self.allowances = allowances
        self.deductions = deductions
    
    def calculate_pay(self, overtime_threshold=40, overtime_multiplier=1.5):
        regular_hours = min(self.hours_worked, overtime_threshold)
        overtime_hours = max(0, self.hours_worked - overtime_threshold)
        base_pay = regular_hours * self.hourly_rate
        overtime_pay = overtime_hours * self.hourly_rate * overtime_multiplier
        gross_pay = base_pay + overtime_pay + self.allowances
        net_pay = gross_pay - self.deductions
        return {
            'regular_hours': regular_hours,
            'overtime_hours': overtime_hours,
            'base_pay': base_pay,
            'overtime_pay': overtime_pay,
            'allowances': self.allowances,
            'deductions': self.deductions,
            'gross_pay': gross_pay,
            'net_pay': net_pay
        }
    
    def to_dict(self):
        return {
            'name': self.name,
            'employee_id': self.employee_id,
            'hourly_rate': self.hourly_rate,
            'hours_worked': self.hours_worked,
            'department': self.department,
            'allowances': self.allowances,
            'deductions': self.deductions
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['employee_id'],
            data['hourly_rate'],
            hours_worked=data.get('hours_worked', 0),
            department=data.get('department', ''),
            allowances=data.get('allowances', 0),
            deductions=data.get('deductions', 0)
        )

class PayrollSystem:
    def __init__(self, data_file='payroll_data.json', overtime_threshold=40, overtime_multiplier=1.5):
        self.data_file = data_file
        self.employees = {}
        self.overtime_threshold = overtime_threshold
        self.overtime_multiplier = overtime_multiplier
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.employees = {
                        emp_id: Employee.from_dict(emp_data)
                        for emp_id, emp_data in data.items()
                    }
            except:
                self.employees = {}
        else:
            self.employees = {}
    
    def save_data(self):
        data = {
            emp_id: emp.to_dict()
            for emp_id, emp in self.employees.items()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_employee(self, name, employee_id, hourly_rate, department='', allowances=0, deductions=0):
        if employee_id in self.employees:
            return False, "Employee ID already exists"
        if hourly_rate < 0:
            return False, "Hourly rate must be positive"
        if allowances < 0 or deductions < 0:
            return False, "Allowances and deductions must be non-negative"
        self.employees[employee_id] = Employee(
            name,
            employee_id,
            hourly_rate,
            department=department,
            allowances=allowances,
            deductions=deductions
        )
        self.save_data()
        return True, f"Employee {name} added successfully"
    
    def remove_employee(self, employee_id):
        if employee_id not in self.employees:
            return False, "Employee not found"
        name = self.employees[employee_id].name
        del self.employees[employee_id]
        self.save_data()
        return True, f"Employee {name} removed successfully"
    
    def update_hours(self, employee_id, hours):
        # Maintained for backward compatibility with older routes/tests
        return self.update_compensation(employee_id, hours=hours)

    def update_compensation(self, employee_id, hours=None, allowances=None, deductions=None):
        if employee_id not in self.employees:
            return False, "Employee not found"
        emp = self.employees[employee_id]
        if hours is not None:
            if hours < 0:
                return False, "Hours worked must be non-negative"
            emp.hours_worked = hours
        if allowances is not None:
            if allowances < 0:
                return False, "Allowances must be non-negative"
            emp.allowances = allowances
        if deductions is not None:
            if deductions < 0:
                return False, "Deductions must be non-negative"
            emp.deductions = deductions
        self.save_data()
        return True, f"Compensation updated for {emp.name}"
    
    def calculate_payroll(self, employee_id=None):
        if employee_id:
            if employee_id not in self.employees:
                return None, "Employee not found"
            emp = self.employees[employee_id]
            breakdown = emp.calculate_pay(self.overtime_threshold, self.overtime_multiplier)
            result = {
                'employee_id': employee_id,
                'name': emp.name,
                'hours': emp.hours_worked,
                'rate': emp.hourly_rate,
                'department': emp.department,
                **breakdown
            }
            return result, None
        else:
            payroll = []
            total_gross = 0
            total_net = 0
            total_hours = 0
            for emp_id, emp in self.employees.items():
                breakdown = emp.calculate_pay(self.overtime_threshold, self.overtime_multiplier)
                payroll.append({
                    'employee_id': emp_id,
                    'name': emp.name,
                    'hours': emp.hours_worked,
                    'rate': emp.hourly_rate,
                    'department': emp.department,
                    **breakdown
                })
                total_hours += emp.hours_worked
                total_gross += breakdown['gross_pay']
                total_net += breakdown['net_pay']
            totals = {
                'gross_total': total_gross,
                'net_total': total_net,
                'total_hours': total_hours
            }
            return payroll, totals
    
    def list_employees(self):
        return list(self.employees.values())

    def get_summary(self):
        payroll, totals = self.calculate_payroll()
        employee_count = len(self.employees)
        avg_rate = 0
        if employee_count:
            avg_rate = sum(emp.hourly_rate for emp in self.employees.values()) / employee_count
        return {
            'employee_count': employee_count,
            'total_hours': totals.get('total_hours', 0),
            'gross_total': totals.get('gross_total', 0),
            'net_total': totals.get('net_total', 0),
            'average_rate': avg_rate
        }

    def export_payroll_csv(self):
        payroll, totals = self.calculate_payroll()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Employee ID', 'Name', 'Department', 'Hours',
            'Regular Hours', 'Overtime Hours', 'Hourly Rate',
            'Base Pay', 'Overtime Pay', 'Allowances', 'Deductions',
            'Gross Pay', 'Net Pay'
        ])
        for row in payroll:
            writer.writerow([
                row['employee_id'],
                row['name'],
                row.get('department', ''),
                f"{row['hours']:.2f}",
                f"{row['regular_hours']:.2f}",
                f"{row['overtime_hours']:.2f}",
                f"{row['rate']:.2f}",
                f"{row['base_pay']:.2f}",
                f"{row['overtime_pay']:.2f}",
                f"{row['allowances']:.2f}",
                f"{row['deductions']:.2f}",
                f"{row['gross_pay']:.2f}",
                f"{row['net_pay']:.2f}",
            ])
        writer.writerow([])
        writer.writerow([
            '', '', '', '', '', '', 'Totals',
            '', '',
            '', '',
            f"{totals.get('gross_total', 0):.2f}",
            f"{totals.get('net_total', 0):.2f}"
        ])
        output.seek(0)
        return output.getvalue()


