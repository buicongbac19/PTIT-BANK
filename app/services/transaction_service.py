from decimal import Decimal

from flask import session

from app.controllers.sendEmail_controller import send_transaction_email
from app.models import Account, Transaction
from werkzeug.security import check_password_hash
from app import db
import uuid
from datetime import datetime


# Kiểm tra và thực hiện giao dịch
def process_transfer(account_id, pin):
    account = Account.query.get(account_id)
    if account:
        # Kiểm tra mã PIN
        if not check_password_hash(account.PinCode, pin):
            return {'success': False, 'message': 'Mã PIN không chính xác.'}

        # Lấy thông tin người nhận
        recipient_account_number = session.get('recipient_account')
        recipient_account = Account.query.filter_by(accountNumber=recipient_account_number).first()

        if recipient_account:
            # Kiểm tra số dư tài khoản
            amount = Decimal((session.get('amount')))
            if account.Balance >= amount:
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
                return {'success': True, 'message': 'Chuyển khoản thành công và email thông báo đã được gửi.'}
            else:
                return {'success': False, 'message': 'Số dư không đủ.'}
        else:
            return {'success': False, 'message': 'Tài khoản người nhận không tồn tại.'}

    return {'success': False, 'message': 'Tài khoản người gửi không tồn tại.'}


# Kiểm tra và khởi tạo chuyển khoản
def initiate_transfer(recipient_account, amount, content):
    if not recipient_account or not amount or not content:
        return {'success': False, 'message': 'Thông tin không đầy đủ.'}

    return {'success': True, 'message': 'Thông tin chuyển khoản hợp lệ.'}
