# services/auth_service.py
from flask import session
from werkzeug.security import generate_password_hash
from app.models import Customer
from app.models import Account
from app import db
import datetime
import uuid


def create_user_account(data):
    # Kiểm tra username và email có tồn tại không
    existing_account = Account.query.filter_by(Username=data['username']).first()
    existing_customer = Customer.query.filter_by(Email=data['email']).first()
    if existing_account or existing_customer:
        return False, "Username or Email already exists!"

    # Mã hóa mật khẩu
    hashed_password = generate_password_hash(data['password'])

    # Tạo bản ghi Customer và Account
    new_customer = Customer(
        CustomerID=str(uuid.uuid4()),  # Hoặc sinh mã tùy ý
        FirstName=data['first_name'],
        LastName=data['last_name'],
        DateOfBirth=data['date_of_birth'],
        Role="user",  # Gán role mặc định
        Email=data['email'],
        PhoneNumber=data['phone_number'],
        Address=data['address'],
        City=data['city'],
        Country=data['country']
    )

    new_account = Account(
        AccountID=str(uuid.uuid4()),
        CustomerID=new_customer.CustomerID,
        Username=data['username'],
        Password=hashed_password,
        Email=data['email'],
        AccountType="savings",  # Gán loại tài khoản mặc định
        Balance=0.0,
        DateOpened=datetime.date.today(),
        Status="Active"
    )

    # Thêm vào cơ sở dữ liệu
    db.session.add(new_customer)
    db.session.add(new_account)
    db.session.commit()
    session['new_account'] = {
        'AccountID': new_account.AccountID,
        'CustomerID': new_customer.CustomerID,
        'Username': new_account.Username,
        'Email': new_account.Email,
        'PhoneNumber': new_customer.PhoneNumber,
    }
    return True, "Account created successfully."
