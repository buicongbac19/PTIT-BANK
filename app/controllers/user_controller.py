from flask import session

def dashboard():    
    from app.services.user_service import dashboard
    return dashboard()

def retrieve_user():
    from app.services.user_service import retrieve_user
    return retrieve_user()

def get_transaction():
    from app.services.user_service import get_transaction
    return get_transaction()

def add_user():
    from app.services.user_service import add_user
    return add_user()

def change_status_account(customer_id):
    from app.services.user_service import change_status_account
    return change_status_account(customer_id)

def update_user(customer_id):
    from app.services.user_service import update_user
    return update_user(customer_id)

def locked_user(customer_id):
    from app.services.user_service import locked_user
    return locked_user(customer_id)

def unlocked_user(customer_id):
    from app.services.user_service import unlocked_user
    return unlocked_user(customer_id)

def search_user():
    from app.services.user_service import search_user
    return search_user()

def login():
    from app.services.user_service import login
    return login()

def start_transfer():
    from app.services.user_service import initiate_transfer
    return initiate_transfer()

def confirm_transaction():
    from app.services.user_service import confirm_transaction
    return confirm_transaction()

def execute_transfer():
    from app.services.user_service import process_transfer
    return process_transfer()

def query_transaction():
    from app.services.user_service import query_transaction
    return query_transaction()

def handle_withdraw_request():
    from app.services.user_service import process_withdrawal
    return process_withdrawal()

def register_user():
    from app.services.user_service import create_user_account
    return create_user_account()