import json
import os
from datetime import datetime

class Employee:
    def __init__(self, name, employee_id, hourly_rate, hours_worked=0):
        self.name = name
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    
    def calculate_pay(self):
        return self.hourly_rate * self.hours_worked
    
    def to_dict(self):
        return {
            'name': self.name,
            'employee_id': self.employee_id,
            'hourly_rate': self.hourly_rate,
            'hours_worked': self.hours_worked
        }
    
    @classmethod
    def from_dict(cls, data):
        emp = cls(data['name'], data['employee_id'], data['hourly_rate'])
        emp.hours_worked = data.get('hours_worked', 0)
        return emp

class PayrollSystem:
    def __init__(self, data_file='payroll_data.json'):
        self.data_file = data_file
        self.employees = {}
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
    
    def add_employee(self, name, employee_id, hourly_rate):
        if employee_id in self.employees:
            return False, "Employee ID already exists"
        self.employees[employee_id] = Employee(name, employee_id, hourly_rate)
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
        if employee_id not in self.employees:
            return False, "Employee not found"
        self.employees[employee_id].hours_worked = hours
        self.save_data()
        return True, f"Hours updated for {self.employees[employee_id].name}"
    
    def calculate_payroll(self, employee_id=None):
        if employee_id:
            if employee_id not in self.employees:
                return None, "Employee not found"
            emp = self.employees[employee_id]
            pay = emp.calculate_pay()
            return {
                'employee_id': employee_id,
                'name': emp.name,
                'hours': emp.hours_worked,
                'rate': emp.hourly_rate,
                'total_pay': pay
            }, None
        else:
            payroll = []
            total = 0
            for emp_id, emp in self.employees.items():
                pay = emp.calculate_pay()
                payroll.append({
                    'employee_id': emp_id,
                    'name': emp.name,
                    'hours': emp.hours_worked,
                    'rate': emp.hourly_rate,
                    'total_pay': pay
                })
                total += pay
            return payroll, total
    
    def list_employees(self):
        return list(self.employees.values())


