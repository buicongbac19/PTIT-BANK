import random
import string

from flask import render_template, request, redirect, url_for

from app import db
from app.models import Account


def generate_account_id(inlength=8):
    return ''.join(random.choices(string.digits, k=inlength))


def retrieving_account_service():
    accounts = Account.query.all()  # Lấy danh sách tất cả các tài khoản từ DB
    return render_template('account_list.html', accounts=accounts)


def CreateAcc_service():
    if request.method == 'POST':
        account_data = {
            "AccountID": generate_account_id(10),
            "Username": request.form['Username'],
            "Password": request.form['Password'],
            "Email": request.form['Email'],
            "AccountType": request.form.get('AccountType', 'standard'),
            "Balance": request.form.get('Balance', 50000),
            "Status": request.form.get('Status', 'active'),
            "PinCode": request.form.get('PinCode'),
            "creditScored": request.form.get('creditScored', 0)
        }
        new_account = Account(**account_data)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('account_list'))


def EditingAcc_service(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    if request.method == 'POST':
        # Cập nhật các thuộc tính từ form
        account.Email = request.form['Email']
        account.AccountType = request.form.get('AccountType', account.AccountType)
        account.Balance = request.form.get('Balance', account.Balance)
        account.Status = request.form.get('Status', account.Status)
        account.PinCode = request.form.get('PinCode', account.PinCode)
        account.creditScored = request.form.get('creditScored', account.creditScored)

        db.session.commit()  # Lưu thay đổi vào DB
        return redirect(url_for('account_list'))


def LockedAcc_service(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    account.Status = 'Locked'
    db.session.commit()  # Xóa tài khoản khỏi DB
    return redirect(url_for('account_list'))


def UnlockedAcc_service(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    account.Status = 'Active'
    db.session.commit()  # Xóa tài khoản khỏi DB
    return redirect(url_for('account_list'))


def SearchAcc_service():
    account_id = request.args.get('AccountID', None)
    account_number = request.args.get('accountNumber', None)

    # Tìm kiếm theo AccountID hoặc accountNumber
    if account_id:
        accounts = Account.query.filter_by(AccountID=account_id).all()
    elif account_number:
        accounts = Account.query.filter_by(accountNumber=account_number).all()
    else:
        accounts = []

    return render_template('account_list.html', accounts=accounts)
