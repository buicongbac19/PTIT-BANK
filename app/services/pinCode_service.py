import re

from flask import request, session, flash, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Account  # Giả sử bạn có model Account đã được định nghĩa


# Service để thêm mã PIN mới
def add_pin_service():
    if request.method == 'POST':
        new_pin = request.form.get('new_pin')
        account_id = session.get('account_id')

        # Kiểm tra xem mã PIN có hợp lệ không
        if not new_pin:
            flash('Mã PIN không thể trống.', "danger")
            return render_template('set_pin.html')

        if not re.match(r"^\d{6}$", new_pin):
            flash('Mã PIN phải là 6 chữ số.', "danger")
            return render_template('set_pin.html')

        # Lấy tài khoản từ cơ sở dữ liệu
        account = Account.query.get(account_id)
        if account:
            if account.PinCode:
                flash('Mã PIN đã tồn tại. Hãy sử dụng chức năng cập nhật.', "danger")
                return render_template('set_pin.html')

            # Mã hóa và lưu mã PIN mới
            account.PinCode = generate_password_hash(new_pin)
            db.session.commit()
            flash('Mã PIN đã được thêm thành công.', "success")
            return redirect(url_for('dashboard'))
        else:
            flash('Tài khoản không tồn tại.', "danger")
            return redirect(url_for('set_pin'))

    return render_template('set_pin.html')


# Service để cập nhật mã PIN
def update_pin_service():
    if request.method == 'POST':
        old_pin = request.form.get('old_pin')
        new_pin = request.form.get('new_pin')
        account_id = session.get('account_id')

        # Kiểm tra độ dài mã PIN mới hợp lệ
        if not re.match(r"^\d{6}$", new_pin):
            flash('Mã PIN mới phải là 6 chữ số.', "danger")
            return render_template('change_pin.html')

        # Lấy tài khoản từ cơ sở dữ liệu
        account = Account.query.get(account_id)
        if account:
            # Kiểm tra mã PIN cũ
            if not check_password_hash(account.PinCode, old_pin):
                flash('Mã PIN cũ không chính xác.', "danger")
                return render_template('change_pin.html')

            # Cập nhật mã PIN mới
            account.PinCode = generate_password_hash(new_pin)
            db.session.commit()
            flash('Mã PIN đã được cập nhật thành công.', "success")
            return redirect(url_for('dashboard'))
        else:
            flash('Tài khoản không tồn tại.', "danger")
            return redirect(url_for('change_pin'))

    return render_template('change_pin.html')
