import random
import string
import re
import unicodedata

from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Account, Customer

from app.controllers.email_controller import send_verification_email


def generate_account_id(id_length=8):
    return "".join(random.choices(string.digits, k=id_length))


def retrieve_account():
    accounts = Account.query.all()  # Lấy danh sách tất cả các tài khoản từ DB
    return render_template("account_list.html", accounts=accounts)


def is_strong_password(password):
    message, category = "", ""
    if len(password) < 8:
        message, category = "Mật khẩu phải có ít nhất 8 ký tự.", "danger"
    elif not any(char.isupper() for char in password):
        message, category = "Mật khẩu phải có ít nhất 1 chữ cái viết hoa.", "danger"
    elif not any(char.islower() for char in password):
        message, category = "Mật khẩu phải có ít nhất 1 chữ cái viết thường.", "danger"
    elif not any(char.isdigit() for char in password):
        message, category = "Mật khẩu phải có ít nhất 1 chữ số.", "danger"
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        message, category = "Mật khẩu phải có ít nhất 1 ký tự đặc biệt.", "danger"
    elif any(char.isspace() for char in password):
        message, category = "Mật khẩu không được chứa khoảng trắng.", "danger"
    else:
        message, category = "Mật khẩu hợp lệ.", "success"
    return message, category


def handle_create_account(data):
    if "Password" in data:
        message, category = is_strong_password(data["Password"])
        if category == "danger":
            return message, category
        data["Password"] = generate_password_hash(data["Password"])
    new_account = Account(**data)
    try:
        db.session.add(new_account)
        db.session.commit()
        return "Account created successfully!", "success"
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}", "danger"


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


def get_detail_account(account_id):
    if not account_id:
        return "Bạn chưa đăng nhập", "danger", [None, None]

    # Truy vấn thông tin tài khoản từ DB dựa trên account_id
    account = Account.query.get(account_id)
    if not account:
        return "Tài khoản không tồn tại", "danger", [None, None]
    customer = Customer.query.filter_by(CustomerID=account.CustomerID).first()
    return "", "success", [account, customer]


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
        return redirect(url_for("auth.register"))
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


def handle_forgot_password(data):
    # Tìm tài khoản theo email
    customer = Customer.query.filter_by(Email=data["email"]).first()
    if customer:
        account = Account.query.filter_by(CustomerID=customer.CustomerID).first()

        # Tạo mã xác thực ngẫu nhiên
        verification_code = str(random.randint(100000, 999999))

        # Lưu mã xác thực và ID tài khoản vào session
        session["verification_code"] = verification_code
        session["account_id"] = account.AccountID

        # Gửi email xác thực
        message, category = send_verification_email(
            data["email"], verification_code, "MÃ XÁC THỰC ĐỔI MẬT KHẨU"
        )

        return message, category
    else:
        # Email không tồn tại trong hệ thống
        return "Email không tồn tại trong hệ thống.", "danger"


def handle_verify_pin(verify_code):
    verification_code = session["verification_code"]
    if verification_code == verify_code:
        return "Mã xác thực chính xác", "success"
    else:
        return "Mã xác thực không đúng, vui lòng kiểm tra lại!", "danger"


def handle_reset_password(new_password, confirm_password):

    if new_password != confirm_password:
        return "Mật khẩu mới và mật khẩu nhập lại không khớp.", "danger"

    # Kiểm tra mã xác thực
    account_id = session.get("account_id")
    account = Account.query.get(account_id)

    if account:
        # Hash và lưu mật khẩu mới
        hashed_password = generate_password_hash(new_password)
        account.Password = hashed_password
        db.session.commit()

        # Xóa ID tài khoản khỏi session
        session.pop("account_id", None)

        return "Mật khẩu đã được thay đổi thành công.", "success"
    else:
        return "Tài khoản không tồn tại.", "danger"


def handle_send_change_email_pin(email):
    if email:
        verification_code = str(random.randint(100000, 999999))
        # Lưu mã xác thực và ID tài khoản vào session
        session["verification_code"] = verification_code
        # Gửi email xác thực
        message, category = send_verification_email(
            email, verification_code, "MÃ XÁC THỰC ĐỔI EMAIL"
        )
        return message, category
    else:
        return "Bạn chưa đăng nhập", "danger"


def handle_change_email(new_email, verify_code):
    verification_code = session["verification_code"]
    if verification_code == verify_code:
        # Kiểm tra email đã tồn tại hay chưa
        if Customer.query.filter_by(Email=new_email).first():
            return "Email đã tồn tại trong hệ thống.", "danger"
        else:
            account_id = session.get("account_id")
            account = Account.query.get(account_id)
            if account:
                customer = Customer.query.filter_by(
                    CustomerID=account.CustomerID
                ).first()
                if customer:
                    customer.Email = new_email
                    db.session.commit()
                    return "Email đã được thay đổi thành công!", "success"
    return "Mã xác thực không chính xác, vui lòng thử lại", "danger"


def handle_send_change_password_pin(email):
    if email:
        verification_code = str(random.randint(100000, 999999))
        # Lưu mã xác thực và ID tài khoản vào session
        session["verification_code"] = verification_code
        # Gửi email xác thực
        message, category = send_verification_email(
            email, verification_code, "MÃ XÁC THỰC ĐỔI MẬT KHẨU"
        )
        return message, category
    else:
        return "Bạn chưa đăng nhập", "danger"


def handle_change_password(old_password, new_password, verify_code):
    account_id = session.get("account_id")
    if not account_id:
        return "Bạn chưa đăng nhập", "danger"
    account = Account.query.get(account_id)
    if not account:
        return "Tài khoản không tồn tại", "danger"
    if not check_password_hash(account.Password, old_password):
        return "Mật khẩu cũ không chính xác", "danger"
    verification_code = session.get("verification_code")
    if not verification_code or verification_code != verify_code:
        return "Mã xác thực không chính xác", "danger"
    hashed_new_password = generate_password_hash(new_password)

    account.Password = hashed_new_password
    db.session.commit()

    session.pop("verification_code", None)

    return "Đổi mật khẩu thành công", "success"


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


def handle_convert_credit_score(amount):
    account_id = session.get("account_id")
    if not account_id:
        return "Bạn chưa đăng nhập", "danger", None
    account = Account.query.filter_by(AccountID=account_id).first()
    if not account:
        return "Tài khoản không tồn tại", "danger", None
    account.creditScored -= int(amount)
    db.session.commit()
    return "Đổi điểm thưởng thành công!", "success", account


def handle_get_profile():
    account_id = session.get("account_id")
    if not account_id:
        return "Bạn chưa đăng nhập", "danger", None, None
    account = Account.query.filter_by(AccountID=account_id).first()
    if not account:
        return "Tài khoản không tồn tại", "danger", None, None
    customer = Customer.query.filter_by(CustomerID=account.CustomerID).first()
    return "Thông tin tài khoản", "success", account, customer


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def handle_choose_account_number(account_number):
    account_id = session.get("account_id")
    if not account_id:
        return "Bạn chưa đăng nhập", "danger"
    account = Account.query.filter_by(AccountID=account_id).first()
    if not account:
        return "Tài khoản không tồn tại", "danger"
    if not account_number:
        return "Số tài khoản không thể trống", "danger"
    if not account_number.isdigit():
        return "Số tài khoản chỉ bao gồm các chữ số", "danger"
    if len(account_number) < 8 or len(account_number) > 16:
        return "Số tài khoản phải có ít nhất 8 và nhiều nhất 16 chữ số", "danger"
    if " " in account_number:
        return "Số tài khoản không được có khoảng trắng", "danger"
    existing_account = Account.query.filter_by(accountNumber=account_number).first()
    if existing_account:
        return "Số tài khoản đã tồn tại", "danger"
    account.accountNumber = account_number
    db.session.commit()
    return "Chọn tài khoản thành công", "success"


def handle_choose_pin_code(pin_code):
    account_id = session.get("account_id")
    if not account_id:
        return "Bạn chưa đăng nhập", "danger"
    account = Account.query.filter_by(AccountID=account_id).first()
    if not account:
        return "Tài khoản không tồn tại", "danger"
    if not pin_code:
        return "Mã pin không thể trống", "danger"
    if not pin_code.isdigit():
        return "Mã pin chỉ bao gồm các chữ số", "danger"
    if len(pin_code) != 6:
        return "Mã pin phải có đúng 6 chữ số!", "danger"
    if " " in pin_code:
        return "Mã pin không được có khoảng trắng", "danger"
    account.PinCode = pin_code
    db.session.commit()
    return "Thiết lập mã pin thành công!", "success"
