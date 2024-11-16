from app.services.account_service import (
    retrieving_account,
    create_account,
    locked_account,
    edit_account,
    unlocked_account,
    search_account,
    set_account_number,
    generate_account_numbers,
    forgot_password,
    reset_password,
    add_pin,
    update_pin,
)


from flask import session


def retrieve_account():
    return retrieving_account()


def create_account():
    return create_account()


def edit_account(account_id):
    return edit_account()


def looked_account(account_id):
    return locked_account(account_id)


def unlooked_account(account_id):
    return unlocked_account(account_id)


def search_account():
    return search_account()


def handle_choose_account_number(account_number):
    return set_account_number(account_number)


# Xử lý tạo danh sách số tài khoản cho trang lựa chọn
def get_available_account_numbers():
    phone_number = session["new_account"]["PhoneNumber"]
    return generate_account_numbers(phone_number)


def forgot_password():
    return forgot_password()


# Controller reset mật khẩu
def reset_password():
    return reset_password()


def add_pin():
    return add_pin()


# Controller để xử lý form đổi mã PIN
def update_pin():
    return update_pin()
