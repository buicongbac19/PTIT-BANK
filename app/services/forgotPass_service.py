import random

from flask import session
from werkzeug.security import generate_password_hash

from app import db
from app.controllers.sendEmail_controller import send_verification_email
from app.models import Account


def forgot_password_service(email):
    account = Account.query.filter_by(Email=email).first()
    if account:
        verification_code = str(random.randint(100000, 999999))
        session['verification_code'] = verification_code
        session['account_id'] = account.AccountID  # Lưu account ID vào session
        send_verification_email(email, verification_code)
        return {'success': True, 'message': 'Mã xác thực đã được gửi đến email của bạn.'}
    return {'success': False, 'message': 'Email không tồn tại trong hệ thống'}


def reset_password_service(verification_code, new_password):
    if session.get('verification_code') == verification_code:
        account_id = session.get('account_id')
        account = Account.query.get(account_id)
        if account:
            # Hash mật khẩu mới
            hashed_password = generate_password_hash(new_password)
            account.Password = hashed_password
            db.session.commit()
            return {'success': True, 'message': 'Mật khẩu đã được thay đổi thành công.'}
        else:
            return {'success': False, 'message': 'Tài khoản không tồn tại.'}
    else:
        return {'success': False, 'message': 'Mã xác thực không đúng.'}
