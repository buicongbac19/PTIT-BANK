from decimal import Decimal

from flask import session, request, redirect, flash, url_for, render_template

from app.controllers.sendEmail_controller import send_transaction_email
from app.models import Account, Transaction
from werkzeug.security import check_password_hash
from app import db
import uuid
from datetime import datetime


# Kiểm tra và thực hiện giao dịch
def process_transfer():
    if request.method == 'POST':
        pin = request.form['pin']
        account_id = session.get('account_id')
        account = Account.query.get(account_id)
        # Kiểm tra mã PIN
        if not check_password_hash(account.PinCode, pin):
            flash('Mã pin không chính xác')
            return render_template('enter_pin.html')

            # Lấy thông tin người nhận
        recipient_account_number = session.get('recipient_account')
        recipient_account = Account.query.filter_by(accountNumber=recipient_account_number).first()
        amount = Decimal((session.get('amount')))
        points_earned = int(amount // 1000)
        account.creditScore += points_earned

                    # Tạo giao dịch
        transaction = Transaction(
                        TransactionID=str(uuid.uuid4()),  # Tạo mã giao dịch duy nhất
                        senderAccountNumber=account.accountNumber,
                        recipientAccountNumber=recipient_account.accountNumber,
                        TransactionDate=datetime.now(),
                        TransactionType="Chuyển khoản nhanh",  # Chuyển khoản
                        Amount=amount,
                        Description=session.get('content')
                    )
        # Lưu giao dịch vào database
        db.session.add(transaction)

         # Cập nhật số dư tài khoản

        account.Balance -= amount
        recipient_account.Balance += amount
        db.session.commit()
        recipient_name = f"{recipient_account.customer.FirstName} {recipient_account.customer.LastName}"
        # Lấy thông tin chi tiết giao dịch để gửi email
        transaction_details = {
                        'recipient_name': recipient_name,  # Tên người nhận từ bảng Customer
                        'recipient_account': recipient_account.accountNumber,
                        'amount': amount,
                        'content': session.get('content'),
                        'transaction_date': transaction.TransactionDate.strftime("%Y-%m-%d %H:%M:%S")
                    }

        # Gửi email thông báo giao dịch
        send_transaction_email(account.Email, transaction_details)
        flash("Chuyển khoản thành công và email thông báo đã được gửi.", "success")
        return render_template('receipt.html', transaction=transaction_details)

    return render_template('enter_pin.html')


# Kiểm tra và khởi tạo chuyển khoản
def initiate_transfer():
    if request.method == 'POST':
        recipient_account = request.form['recipient_account']
        amountstr = request.form['amount']
        amount = Decimal(amountstr)
        content = request.form['content']
        account_id = session.get('account_id')
        # Kiểm tra thông tin chuyển khoản
        if not recipient_account or not amount or not content:
            flash("Vui lòng nhập đầy đủ thông tin ", "danger")

        account_recip = Account.query.get(recipient_account)
        account_send = Account.query.get(account_id)
        if not account_recip:
            flash("Tài khoản người nhận không tồn tại!")
            return redirect(url_for('transfer'))
        if account_send.balance < amount:
            flash('Số dư tài khoản không đủ để thực hiện giao dịch')
            return redirect(url_for('transfer'))
        # Lưu thông tin vào session cho bước xác nhận
        session['recipient_account'] = recipient_account
        session['amount'] = amount
        session['content'] = content

    return render_template('transfer_form.html')


def confirm_trans_service():
    if request.method == 'POST':
        return redirect(url_for('enter_pin'))

    recipient_account = session.get('recipient_account')
    amount = session.get('amount')
    content = session.get('content')
    return render_template('confirm_transfer.html', recipient_account=recipient_account, amount=amount, content=content)
