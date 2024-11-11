from flask import session, flash, redirect, url_for

from app.services.choose_account_service import set_account_number, generate_account_numbers


def handle_choose_account_number(account_number):
    # Lấy thông tin tài khoản từ session, account_info là từ điển chứa thông tin tài khoản
    account_info = session.get('new_account')

    if not account_info:
        flash("Không tìm thấy thông tin tài khoản trong session.", "danger")
        return redirect(url_for('register'))  # Hoặc trang khác nếu không có tài khoản trong session

    account_id = account_info['AccountID']  # Lấy AccountID từ từ điển trong session

    if set_account_number(account_id, account_number):
        flash("Số tài khoản đã được chọn thành công!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Lỗi khi chọn số tài khoản.", "danger")
        return redirect(url_for('choose_account_number'))


# Xử lý tạo danh sách số tài khoản cho trang lựa chọn
def get_available_account_numbers():
    phone_number = session['new_account']['PhoneNumber']
    return generate_account_numbers(phone_number)
