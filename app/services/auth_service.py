# services/auth_service.py
from flask import session, request, flash, redirect, render_template, url_for
from werkzeug.security import generate_password_hash
from app.models import Customer
from app.models import Account
from app import db
from datetime import datetime
import uuid

from app.services.validate_service import is_valid_email, is_valid_username, is_valid_phone_number


def create_user_account():
    if request.method == 'POST':
        data = {
            "username": request.form['username'],
            "password": request.form['password'],
            "confirm_password": request.form['confirm_password'],
            "email": request.form['email'],
            "phone_number": request.form['phoneNumber'],
            "first_name": request.form['firstName'],
            "last_name": request.form['lastName'],
            "date_of_birth": datetime.strptime(request.form['dateOfBirth'], '%Y-%m-%d').date(),
            "address": request.form['address'],
            "city": request.form['city'],
            "country": request.form['country']
        }
        # Kiểm tra định dạng email hợp lệ
        if not is_valid_email(data['email']):
            flash('Email không hợp lệ!', 'danger')
            return redirect(url_for('register'))  # Quay lại trang đăng ký

        # Kiểm tra username không có khoảng trắng
        if not is_valid_username(data['username']):
            flash('Tên đăng nhập không hợp lệ!', 'danger')
            return redirect(url_for('register'))

        # Kiểm tra số điện thoại hợp lệ
        if not is_valid_phone_number(data['phone_number']):
            flash('Số điện thoại không hợp lệ!', 'danger')
            return redirect(url_for('register'))
        # Kiểm tra username và email có tồn tại không
        existing_account = Account.query.filter_by(Username=data['username']).first()
        existing_customer = Customer.query.filter_by(Email=data['email']).first()
        if existing_account:
            return False, "Tài khoản đã tồn tại!"
        elif existing_customer:
            return False, "Email đã tồn tại!"

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(data['password'])

        # Tạo bản ghi Customer và Account
        new_customer = Customer(
            CustomerID=str(uuid.uuid4()),
            FirstName=data['first_name'],
            LastName=data['last_name'],
            DateOfBirth=data['date_of_birth'],
            Role="User",
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
            AccountType="savings",
            creditScored=0,
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
        flash("Đăng ký thành công!")
        return redirect('/choose_account_number')

    return render_template('register.html')
