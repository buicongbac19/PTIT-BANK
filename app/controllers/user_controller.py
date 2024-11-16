from app.services.user_service import (
    retrieve_user,
    add_user,
    change_status_account,
    update_user,
    locked_user,
    unlocked_user,
    search_user,
    login,
    initiate_transfer,
    confirm_transaction,
    process_transfer,
    query_transaction,
    process_withdrawal,
    create_user_account,
)


def retrieve_user():
    return retrieve_user()


def add_user():
    return add_user()


def change_status_account(customer_id):
    return change_status_account(customer_id)


def update_user(customer_id):
    return update_user(customer_id)


def locked_user(customer_id):
    return locked_user(customer_id)


def unlocked_user(customer_id):
    return unlocked_user(customer_id)


def search_user():
    return search_user()


def login():
    return login()


def start_transfer():
    return initiate_transfer()


def confirm_transaction():
    return confirm_transaction()


# Controller để xử lý giao dịch và kiểm tra mã PIN
def execute_transfer():
    return process_transfer()


def get_transaction():
    return query_transaction()


def handle_withdraw_request():
    return process_withdrawal()


def register_user():
    create_user_account()
