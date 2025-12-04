from flask import Flask, render_template, request, redirect, url_for, flash
from payroll import PayrollSystem

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
payroll = PayrollSystem()

@app.route('/')
def index():
    employees = payroll.list_employees()
    payroll_list, total = payroll.calculate_payroll()
    return render_template('index.html', employees=employees, payroll_list=payroll_list, total=total)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form.get('name', '').strip()
    employee_id = request.form.get('employee_id', '').strip()
    try:
        hourly_rate = float(request.form.get('hourly_rate', 0))
        success, message = payroll.add_employee(name, employee_id, hourly_rate)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Invalid hourly rate. Please enter a number.', 'error')
    return redirect(url_for('index'))

@app.route('/remove_employee/<employee_id>')
def remove_employee(employee_id):
    success, message = payroll.remove_employee(employee_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))

@app.route('/update_hours', methods=['POST'])
def update_hours():
    employee_id = request.form.get('employee_id', '').strip()
    try:
        hours = float(request.form.get('hours', 0))
        success, message = payroll.update_hours(employee_id, hours)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Invalid hours. Please enter a number.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


