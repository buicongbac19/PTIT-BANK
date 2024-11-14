from flask import session, flash, redirect, url_for

from app.services.choose_account_service import set_account_number, generate_account_numbers


def handle_choose_account_number(account_number):
    return set_account_number(account_number)


# Xử lý tạo danh sách số tài khoản cho trang lựa chọn
def get_available_account_numbers():
    phone_number = session['new_account']['PhoneNumber']
    return generate_account_numbers(phone_number)
