from flask import redirect, url_for, session, flash, request, render_template
from app.controllers.transaction_controller import start_transfer, execute_transfer

from app import app


# Route để điền thông tin chuyển khoản
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        # Gọi controller để xử lý logic chuyển khoản
        result = start_transfer(request.form)

        if result['success']:
            return redirect(url_for('confirm'))
        else:
            flash(result['message'], 'danger')

    return render_template('transfer_form.html')


# Route để xác nhận thông tin chuyển khoản
@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        return redirect(url_for('enter_pin'))

    # Lấy thông tin từ session
    recipient_account = session.get('recipient_account')
    amount = session.get('amount')
    content = session.get('content')

    return render_template('confirm_transfer.html', recipient_account=recipient_account, amount=amount, content=content)


# Route để nhập mã PIN và thực hiện giao dịch
@app.route('/enter_pin', methods=['GET', 'POST'])
def enter_pin():
    if request.method == 'POST':
        pin = request.form['pin']
        account_id = session.get('account_id')

        # Gọi service để kiểm tra mã PIN và thực hiện giao dịch
        result = execute_transfer(account_id, pin)
        if result['success']:
            flash('Chuyển khoản thành công!', 'success')
            return 'Thanh cong ròi'
        #render_template('receipt.html')
        else:
            flash(result['message'], 'danger')

    return render_template('enter_pin.html')
