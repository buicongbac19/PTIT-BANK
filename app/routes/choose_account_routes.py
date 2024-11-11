from flask import request, render_template

from app import app
from app.controllers.choose_account_controller import handle_choose_account_number, get_available_account_numbers


@app.route('/choose_account_number', methods=['GET', 'POST'])
def choose_account_number():
    if request.method == 'POST':
        chosen_account_number = request.form.get('account_number')
        return handle_choose_account_number(chosen_account_number)

    # Hiển thị danh sách số tài khoản cho người dùng lựa chọn
    account_numbers = get_available_account_numbers()
    return render_template('choose_account_number.html', account_numbers=account_numbers)
