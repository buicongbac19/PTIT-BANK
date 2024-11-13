import random
import string

from flask import render_template, request, redirect, url_for, flash, render_template_string

from app import db
from app.models import Customer, Account


def generate_account_id(inlength=8):
    return ''.join(random.choices(string.digits, k=inlength))


def retrieving_user_service():
    users = db.session.query(Customer, Account.Status).join(Account, Customer.Email == Account.Email).all()
    return render_template('user_list.html', customers=users)


def add_user_service():
    # Lấy dữ liệu từ biểu mẫu
    customer_id = request.form['CustomerID']
    first_name = request.form['FirstName']
    last_name = request.form['LastName']
    date_of_birth = request.form.get('DateOfBirth')
    role = request.form['Role']
    email = request.form['Email']
    phone_number = request.form['PhoneNumber']
    address = request.form.get('Address')
    city = request.form.get('City')
    country = request.form.get('Country')
    notes = request.form.get('Notes')

    # Tạo đối tượng Customer mới
    new_customer = Customer(
        CustomerID=customer_id,
        FirstName=first_name,
        LastName=last_name,
        DateOfBirth=date_of_birth,
        Role=role,
        Email=email,
        PhoneNumber=phone_number,
        Address=address,
        City=city,
        Country=country,
        Notes=notes
    )

    # Lưu vào cơ sở dữ liệu
    db.session.add(new_customer)
    db.session.commit()

    return redirect(url_for('user_list'))


def change_status_account_service(customer_id):
    # Lấy trạng thái mới từ form data
    new_status = request.form.get('status')

    # Tìm account bằng customer_id
    account = Account.query.filter_by(CustomerID=customer_id).first()

    if account:
        account.Status = new_status
        db.session.commit()
        flash("Trạng thái tài khoản đã được cập nhật.")
    else:
        flash("Không tìm thấy tài khoản.")

    # Quay lại trang quản lý khách hàng sau khi cập nhật
    return redirect(url_for('user_list'))


def updating_user_service(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return "Khong tim thay khach hang", 404
    # Lấy dữ liệu từ biểu mẫu để cập nhật
    customer.FirstName = request.form['FirstName']
    customer.LastName = request.form['LastName']
    customer.DateOfBirth = request.form.get('DateOfBirth')
    customer.Role = request.form['Role']
    customer.Email = request.form['Email']
    customer.PhoneNumber = request.form['PhoneNumber']
    customer.Address = request.form.get('Address')
    customer.City = request.form.get('City')
    customer.Country = request.form.get('Country')
    customer.Notes = request.form.get('Notes')

    # Lưu thay đổi vào cơ sở dữ liệu
    db.session.commit()
    return redirect(url_for('user_list'))


def locked_user_service(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return 'Khong tim thay khach hang', 404
    account = Account.query.filter_by(AccountID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404
    # Cập nhật trạng thái tài khoản thành 'Locked'
    account.Status = 'Locked'
    db.session.commit()
    return redirect(url_for('user_list'))


def unlocked_user_service(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return "User not found", 404
    account = Account.query.filter_by(AccountID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404

    # Cập nhật trạng thái tài khoản thành 'Active'
    account.Status = 'Active'
    db.session.commit()
    return redirect(url_for('user_list'))


def locking_for_user_service():
    customer_id = request.args.get('customerID')
    phone_number = request.args.get('phoneNumber')
    customer = None
    if customer_id:
        customer = Customer.query.filter_by(CustomerID=customer_id).all()
    elif phone_number:
        customer = Customer.query.filter_by(PhoneNumber=phone_number).all()
    # Trả về trang HTML với thông tin khách hàng nếu tìm thấy
    if customer:
        return render_template('user_list.html', customers=customer)
    else:
        return "<h3>Không tìm thấy khách hàng với thông tin đã nhập.</h3>", 404
