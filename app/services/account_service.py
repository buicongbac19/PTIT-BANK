import random
import string
import re

from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Account

from app.controllers.email_controller import send_verification_email


def generate_account_id(inlength=8):
    return "".join(random.choices(string.digits, k=inlength))


def retrieving_account():
    accounts = Account.query.all()  # Lấy danh sách tất cả các tài khoản từ DB
    return render_template("account_list.html", accounts=accounts)


def create_account():
    if request.method == "POST":
        account_data = {
            "AccountID": generate_account_id(10),
            "Username": request.form["Username"],
            "Password": request.form["Password"],
            "Email": request.form["Email"],
            "AccountType": request.form.get("AccountType", "standard"),
            "Balance": request.form.get("Balance", 50000),
            "Status": request.form.get("Status", "active"),
            "PinCode": request.form.get("PinCode"),
            "creditScored": request.form.get("creditScored", 0),
        }
        new_account = Account(**account_data)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for("account_list"))


def edit_account(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    if request.method == "POST":
        # Cập nhật các thuộc tính từ form
        account.Email = request.form["Email"]
        account.AccountType = request.form.get("AccountType", account.AccountType)
        account.Balance = request.form.get("Balance", account.Balance)
        account.Status = request.form.get("Status", account.Status)
        account.PinCode = request.form.get("PinCode", account.PinCode)
        account.creditScored = request.form.get("creditScored", account.creditScored)

        db.session.commit()  # Lưu thay đổi vào DB
        return redirect(url_for("account_list"))


def locked_account(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    account.Status = "Locked"
    db.session.commit()  # Xóa tài khoản khỏi DB
    return redirect(url_for("account_list"))


def unlocked_account(account_id):
    account = Account.query.get(account_id)  # Lấy thông tin tài khoản từ DB
    if not account:
        return "Account not found", 404

    account.Status = "Active"
    db.session.commit()  # Xóa tài khoản khỏi DB
    return redirect(url_for("account_list"))


def search_account():
    account_id = request.args.get("AccountID", None)
    account_number = request.args.get("accountNumber", None)

    # Tìm kiếm theo AccountID hoặc accountNumber
    if account_id:
        accounts = Account.query.filter_by(AccountID=account_id).all()
    elif account_number:
        accounts = Account.query.filter_by(accountNumber=account_number).all()
    else:
        accounts = []

    return render_template("account_list.html", accounts=accounts)


def generate_account_numbers(phone_number, quantity=10):
    account_numbers = [phone_number]
    while len(account_numbers) < quantity:
        new_account = str(random.randint(1000000000, 9999999999))
        if not Account.query.filter_by(accountNumber=new_account).first():
            account_numbers.append(new_account)
    return account_numbers


# Lưu số tài khoản người dùng chọn vào database
def set_account_number(account_number):
    account_info = session.get("new_account")
    if not account_info:
        flash("Không tìm thấy thông tin tài khoản ", "danger")
        return redirect(url_for("register"))
    account_id = account_info["AccountID"]
    # Cập nhật số tài khoản trong cơ sở dữ liệu
    account = Account.query.get(account_id)
    if account:
        account.accountNumber = account_number
        db.session.commit()
        flash("Số tài khoản đã được chọn thành công!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Lỗi khi chọn số tài khoản.", "danger")
        return redirect(url_for("choose_account_number"))


def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        # Tìm tài khoản theo email
        account = Account.query.filter_by(email=email).first()

        if account:
            # Tạo mã xác thực ngẫu nhiên
            verification_code = str(random.randint(100000, 999999))

            # Lưu mã xác thực và ID tài khoản vào session
            session["verification_code"] = verification_code
            session["account_id"] = account.accountID

            # Gửi email xác thực
            send_verification_email(email, verification_code)

            # Thông báo thành công và chuyển hướng
            flash("Mã xác thực đã được gửi đến email của bạn.", "success")
            return redirect(url_for("reset_password"))
        else:
            # Email không tồn tại trong hệ thống
            flash("Email không tồn tại trong hệ thống.", "danger")

    return render_template("forgot_password.html")


def reset_password():
    if request.method == "POST":
        verification_code = request.form["verification_code"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Mật khẩu mới và mật khẩu nhập lại không khớp.", "danger")
            return render_template("reset_password.html")

        # Kiểm tra mã xác thực
        if session.get("verification_code") == verification_code:
            account_id = session.get("account_id")
            account = Account.query.get(account_id)

            if account:
                # Hash và lưu mật khẩu mới
                hashed_password = generate_password_hash(new_password)
                account.Password = hashed_password
                db.session.commit()

                # Xóa mã xác thực và ID tài khoản khỏi session
                session.pop("verification_code", None)
                session.pop("account_id", None)

                flash("Mật khẩu đã được thay đổi thành công.", "success")
                return redirect(url_for("login"))
            else:
                flash("Tài khoản không tồn tại.", "danger")
        else:
            flash("Mã xác thực không đúng.", "danger")

    return render_template("reset_password.html")


def add_pin():
    if request.method == "POST":
        new_pin = request.form.get("new_pin")
        account_id = session.get("account_id")

        # Kiểm tra xem mã PIN có hợp lệ không
        if not new_pin:
            flash("Mã PIN không thể trống.", "danger")
            return render_template("set_pin.html")

        if not re.match(r"^\d{6}$", new_pin):
            flash("Mã PIN phải là 6 chữ số.", "danger")
            return render_template("set_pin.html")

        # Lấy tài khoản từ cơ sở dữ liệu
        account = Account.query.get(account_id)
        if account:
            if account.PinCode:
                flash("Mã PIN đã tồn tại. Hãy sử dụng chức năng cập nhật.", "danger")
                return render_template("set_pin.html")

            # Mã hóa và lưu mã PIN mới
            account.PinCode = generate_password_hash(new_pin)
            db.session.commit()
            flash("Mã PIN đã được thêm thành công.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Tài khoản không tồn tại.", "danger")
            return redirect(url_for("set_pin"))

    return render_template("set_pin.html")


# Service để cập nhật mã PIN
def update_pin():
    if request.method == "POST":
        old_pin = request.form.get("old_pin")
        new_pin = request.form.get("new_pin")
        account_id = session.get("account_id")

        # Kiểm tra độ dài mã PIN mới hợp lệ
        if not re.match(r"^\d{6}$", new_pin):
            flash("Mã PIN mới phải là 6 chữ số.", "danger")
            return render_template("change_pin.html")

        # Lấy tài khoản từ cơ sở dữ liệu
        account = Account.query.get(account_id)
        if account:
            # Kiểm tra mã PIN cũ
            if not check_password_hash(account.PinCode, old_pin):
                flash("Mã PIN cũ không chính xác.", "danger")
                return render_template("change_pin.html")

            # Cập nhật mã PIN mới
            account.PinCode = generate_password_hash(new_pin)
            db.session.commit()
            flash("Mã PIN đã được cập nhật thành công.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Tài khoản không tồn tại.", "danger")
            return redirect(url_for("change_pin"))

    return render_template("change_pin.html")
