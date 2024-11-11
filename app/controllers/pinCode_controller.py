from flask import request, session, redirect, url_for, flash, render_template
from app.services.pinCode_service import add_pin_service, update_pin_service


# Controller để xử lý form thêm mã PIN
def add_pin_controller():
    if request.method == 'POST':
        new_pin = request.form.get('new_pin')
        account_id = session.get('account_id')

        # Gọi service để thêm mã PIN
        result = add_pin_service(account_id, new_pin)
        flash(result['message'], "success" if result['success'] else "danger")
        return redirect(url_for('dashboard'))

    return render_template('set_pin.html')


# Controller để xử lý form đổi mã PIN
def update_pin_controller():
    if request.method == 'POST':
        old_pin = request.form.get('old_pin')
        new_pin = request.form.get('new_pin')
        account_id = session.get('account_id')

        # Gọi service để cập nhật mã PIN
        result = update_pin_service(account_id, old_pin, new_pin)
        flash(result['message'], "success" if result['success'] else "danger")
        return redirect(url_for('dashboard'))

    return render_template('change_pin.html')
