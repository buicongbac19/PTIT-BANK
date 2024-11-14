from flask import redirect, url_for, session, flash, request, render_template
from app.controllers.transaction_controller import start_transfer, execute_transfer, confirm_trans_controller

from app import app


# Route để điền thông tin chuyển khoản
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    return start_transfer()


# Route để xác nhận thông tin chuyển khoản
@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    return confirm_trans_controller()


# Route để nhập mã PIN và thực hiện giao dịch
@app.route('/enter_pin', methods=['GET', 'POST'])
def enter_pin():
    return execute_transfer()
