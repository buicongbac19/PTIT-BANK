from decimal import Decimal

from flask import request, render_template, session, flash, redirect, url_for

from app.controllers.sendEmail_controller import send_withdrawtransaction_email
from app.models import Account, Transaction
from werkzeug.security import check_password_hash
from app import db
import uuid
from datetime import datetime


def process_withdrawal():
    if request.method == 'POST':
        data = request.form  # Sử dụng request.form để nhận dữ liệu từ form POST
        pin = data.get('pin')
        amount = data.get('amount')
        account_id = session.get('account_id')
        if not account_id or not pin or not amount:
            return "Vui long nhập đủ thông tin", 400
        account = Account.query.get(account_id)
        # Kiểm tra mã PIN
        if not check_password_hash(account.PinCode, pin):
            flash('Mã pin không chính xác')
            return redirect(url_for('withdraw'))

        # Kiểm tra số dư tài khoản và số tiền rút
        amount = Decimal(amount)
        if amount < 100000:
            return {'success': False, 'message': 'Số tiền rút phải từ 100,000 VND.'}
        if account.Balance >= amount:
            # Tạo bản ghi giao dịch
            transaction = Transaction(
                TransactionID=str(uuid.uuid4()),
                senderAccountNumber=account.accountNumber,
                recipientAccountNumber=None,
                TransactionDate=datetime.now(),
                TransactionType="Rút tiền",
                Amount=amount,
                Description="Rút tiền từ tài khoản"
            )

            # Lưu giao dịch và cập nhật số dư
            db.session.add(transaction)
            account.Balance -= amount
            db.session.commit()
            withdraw_name = f"{account.customer.FirstName} {account.customer.LastName}"
            transaction_details = {
                'withdrawer': withdraw_name,  # Tên người nhận từ bảng Customer
                'withdraw_account': account.accountNumber,
                'amount': amount,
                'transaction_date': transaction.TransactionDate.strftime("%Y-%m-%d %H:%M:%S")
            }
            send_withdrawtransaction_email(account.Email, transaction_details)

            flash('Rút tiền thành công! Vui lòng kiểm tra email')
            return render_template('receip_withdraw')
        else:
            flash('Số dư không đủ để rút!')
            return redirect(url_for('withdraw'))

    return render_template("withdraw.html")
