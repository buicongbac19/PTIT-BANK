from app.services.transaction_service import initiate_transfer, process_transfer
from flask import session


# Controller để khởi tạo chuyển khoản
def start_transfer(form_data):
    recipient_account = form_data['recipient_account']
    amount = form_data['amount']
    content = form_data['content']

    # Lưu thông tin vào session để sử dụng cho bước xác nhận
    session['recipient_account'] = recipient_account
    session['amount'] = amount
    session['content'] = content

    return initiate_transfer(recipient_account, amount, content)


# Controller để xử lý giao dịch và kiểm tra mã PIN
def execute_transfer(account_id, pin):
    return process_transfer(account_id, pin)
