from flask import session

def retrieve_account():
    from app.services.account_service import retrieving_account
    return retrieving_account()  

def create_account():
    from app.services.account_service import create_account
    return create_account()

def edit_account(account_id):
    from app.services.account_service import edit_account
    return edit_account(account_id)

def recharge_account(account_id):
    from app.services.account_service import recharge_account
    return recharge_account(account_id)

def locked_account(account_id):
    from app.services.account_service import locked_account
    return locked_account(account_id)

def unlocked_account(account_id):
    from app.services.account_service import unlocked_account
    return unlocked_account(account_id)

def search_account():
    from app.services.account_service import search_account
    return search_account()

def handle_choose_account_number(account_number):
    from app.services.account_service import set_account_number
    return set_account_number(account_number)

def get_available_account_numbers():
    from app.services.account_service import generate_account_numbers
    return generate_account_numbers()

def forgot_password():
    from app.services.account_service import forgot_password
    return forgot_password()

def reset_password():
    from app.services.account_service import reset_password
    return reset_password()

def add_pin():
    from app.services.account_service import add_pin
    return add_pin()

def update_pin():
    from app.services.account_service import update_pin
    return update_pin()