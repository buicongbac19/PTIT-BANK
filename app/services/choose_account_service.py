import random

from flask import session, flash, redirect, url_for

from app import db
from app.models import Account


def generate_account_numbers(phone_number, quantity=10):
    account_numbers = [phone_number]
    while len(account_numbers) < quantity:
        new_account = str(random.randint(1000000000, 9999999999))
        if not Account.query.filter_by(accountNumber=new_account).first():
            account_numbers.append(new_account)
    return account_numbers


# Lưu số tài khoản người dùng chọn vào database
def set_account_number(account_number):
    account_info = session.get('new_account')
    if not account_info:
        flash("Không tìm thấy thông tin tài khoản ", "danger")
        return redirect(url_for('register'))
    account_id = account_info['AccountID']
    # Cập nhật số tài khoản trong cơ sở dữ liệu
    account = Account.query.get(account_id)
    if account:
        account.accountNumber = account_number
        db.session.commit()
        flash("Số tài khoản đã được chọn thành công!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Lỗi khi chọn số tài khoản.", "danger")
        return redirect(url_for('choose_account_number'))


