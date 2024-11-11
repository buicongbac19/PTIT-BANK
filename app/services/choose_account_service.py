import random

from app import db
from app.models import Account


def generate_account_numbers(phone_number, quantity=10):
    account_numbers = [phone_number]
    while len(account_numbers) < quantity:
        new_account = str(random.randint(1000000000, 9999999999))
        if not Account.query.filter_by(accountNumber=new_account).first():
            account_numbers.append(new_account)
    return account_numbers


# Lưu số tài khoản người dùng chọn vào database
def set_account_number(account_id, chosen_account_number):
    account = Account.query.get(account_id)
    if account:
        account.accountNumber = chosen_account_number
        db.session.commit()
        return True
    return False
