from app.routes.transaction_routes import transfer
from app.services.transaction_service import initiate_transfer, process_transfer, confirm_trans_service
from flask import session, request


# Controller để khởi tạo chuyển khoản
def start_transfer():
    return initiate_transfer()


def confirm_trans_controller():
    return confirm_trans_service()


# Controller để xử lý giao dịch và kiểm tra mã PIN
def execute_transfer():
    return process_transfer()
