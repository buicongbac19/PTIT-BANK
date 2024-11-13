import random

from flask import session, request, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash

from app import db
from app.controllers.sendEmail_controller import send_verification_email
from app.models import Account


def forgot_password_service():
    if request.method == 'POST':
        email = request.form['email']

        # Tìm tài khoản theo email
        account = Account.query.filter_by(email=email).first()

        if account:
            # Tạo mã xác thực ngẫu nhiên
            verification_code = str(random.randint(100000, 999999))

            # Lưu mã xác thực và ID tài khoản vào session
            session['verification_code'] = verification_code
            session['account_id'] = account.accountID

            # Gửi email xác thực
            send_verification_email(email, verification_code)

            # Thông báo thành công và chuyển hướng
            flash('Mã xác thực đã được gửi đến email của bạn.', "success")
            return redirect(url_for('reset_password'))
        else:
            # Email không tồn tại trong hệ thống
            flash('Email không tồn tại trong hệ thống.', "danger")

    return render_template('forgot_password.html')


def reset_password_service():
    if request.method == 'POST':
        verification_code = request.form['verification_code']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Mật khẩu mới và mật khẩu nhập lại không khớp.", "danger")
            return render_template('reset_password.html')

        # Kiểm tra mã xác thực
        if session.get('verification_code') == verification_code:
            account_id = session.get('account_id')
            account = Account.query.get(account_id)

            if account:
                # Hash và lưu mật khẩu mới
                hashed_password = generate_password_hash(new_password)
                account.Password = hashed_password
                db.session.commit()

                # Xóa mã xác thực và ID tài khoản khỏi session
                session.pop('verification_code', None)
                session.pop('account_id', None)

                flash('Mật khẩu đã được thay đổi thành công.', "success")
                return redirect(url_for('login'))
            else:
                flash('Tài khoản không tồn tại.', "danger")
        else:
            flash('Mã xác thực không đúng.', "danger")

    return render_template('reset_password.html')

