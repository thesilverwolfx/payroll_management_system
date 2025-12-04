from flask import Flask, render_template, request, redirect, url_for, flash, Response
from payroll import PayrollSystem

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
payroll = PayrollSystem()

@app.route('/')
def index():
    employees = payroll.list_employees()
    payroll_list, totals = payroll.calculate_payroll()
    summary = payroll.get_summary()
    return render_template(
        'index.html',
        employees=employees,
        payroll_list=payroll_list,
        totals=totals,
        summary=summary
    )

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form.get('name', '').strip()
    employee_id = request.form.get('employee_id', '').strip()
    department = request.form.get('department', '').strip()
    try:
        hourly_rate = float(request.form.get('hourly_rate', 0))
        allowances = float(request.form.get('allowances', 0) or 0)
        deductions = float(request.form.get('deductions', 0) or 0)
        success, message = payroll.add_employee(
            name,
            employee_id,
            hourly_rate,
            department=department,
            allowances=allowances,
            deductions=deductions
        )
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Invalid numeric input. Please check the values entered.', 'error')
    return redirect(url_for('index'))

@app.route('/remove_employee/<employee_id>')
def remove_employee(employee_id):
    success, message = payroll.remove_employee(employee_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))

def _parse_optional_float(value):
    value = value.strip() if isinstance(value, str) else value
    if value in (None, ''):
        return None
    return float(value)

@app.route('/update_compensation', methods=['POST'])
@app.route('/update_hours', methods=['POST'])
def update_compensation():
    employee_id = request.form.get('employee_id', '').strip()
    try:
        hours = _parse_optional_float(request.form.get('hours', ''))
        allowances = _parse_optional_float(request.form.get('allowances', ''))
        deductions = _parse_optional_float(request.form.get('deductions', ''))
        success, message = payroll.update_compensation(
            employee_id,
            hours=hours,
            allowances=allowances,
            deductions=deductions
        )
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Invalid numeric input. Please check the values entered.', 'error')
    return redirect(url_for('index'))

@app.route('/export_payroll')
def export_payroll():
    csv_content = payroll.export_payroll_csv()
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=payroll_report.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)


