import random
import string
from decimal import Decimal
from sqlalchemy import or_
import re

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    render_template_string,
    session,
)

from app.controllers.email_controller import (
    send_transaction_email,
    send_withdraw_transaction_email,
)
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from app import db
from app.models import Customer, Account, Transaction


def generate_account_id(id_length=8):
    return "".join(random.choices(string.digits, k=id_length))


def get_list_user():
    users = (
        db.session.query(Customer, Account.Status)
        .join(Account, Customer.Email == Account.Email)
        .all()
    )
    return render_template("user_list.html", customers=users)


def handle_create_user(data):
    try:
        # Chuyển đổi ngày sinh từ chuỗi sang datetime.date
        if data["date_of_birth"]:  # Kiểm tra nếu ngày sinh được cung cấp
            data["date_of_birth"] = datetime.strptime(
                data["date_of_birth"], "%d/%m/%Y"
            ).date()
        else:
            data["date_of_birth"] = None
    except ValueError:
        return "Vui lòng nhập ngày sinh theo dạng dd/MM/yyyy.", "danger", None

    # Tạo đối tượng Customer mới
    new_customer = Customer(
        CustomerID=data["customer_id"],
        FirstName=data["first_name"],
        LastName=data["last_name"],
        DateOfBirth=data["date_of_birth"],
        Role=data["role"],
        Email=data["email"],
        PhoneNumber=data["phone_number"],
        Address=data["address"],
        City=data["city"],
        Country=data["country"],
        Notes=data["notes"],
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
        return "Customer registered successfully!", "success", data["customer_id"]
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}", "danger", None


def change_status_account(customer_id):
    # Lấy trạng thái mới từ form data
    new_status = request.form.get("status")

    # Tìm account bằng customer_id
    account = Account.query.filter_by(CustomerID=customer_id).first()

    if account:
        account.Status = new_status
        db.session.commit()
        flash("Trạng thái tài khoản đã được cập nhật.")
    else:
        flash("Không tìm thấy tài khoản.")

    # Quay lại trang quản lý khách hàng sau khi cập nhật
    return redirect(url_for("user_list"))


def update_user(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return "Khong tim thay khach hang", 404
    # Lấy dữ liệu từ biểu mẫu để cập nhật
    customer.FirstName = request.form["FirstName"]
    customer.LastName = request.form["LastName"]
    customer.DateOfBirth = request.form.get("DateOfBirth")
    customer.Role = request.form["Role"]
    customer.Email = request.form["Email"]
    customer.PhoneNumber = request.form["PhoneNumber"]
    customer.Address = request.form.get("Address")
    customer.City = request.form.get("City")
    customer.Country = request.form.get("Country")
    customer.Notes = request.form.get("Notes")

    # Lưu thay đổi vào cơ sở dữ liệu
    db.session.commit()
    return redirect(url_for("user_list"))


def locked_user(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return "Khong tim thay khach hang", 404
    account = Account.query.filter_by(AccountID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404
    # Cập nhật trạng thái tài khoản thành 'Locked'
    account.Status = "Locked"
    db.session.commit()
    return redirect(url_for("user_list"))


def unlocked_user(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return "User not found", 404
    account = Account.query.filter_by(AccountID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404

    # Cập nhật trạng thái tài khoản thành 'Active'
    account.Status = "Active"
    db.session.commit()
    return redirect(url_for("user_list"))


def search_user():
    customer_id = request.args.get("customerID")
    phone_number = request.args.get("phoneNumber")
    customer = None
    if customer_id:
        customer = Customer.query.filter_by(CustomerID=customer_id).all()
    elif phone_number:
        customer = Customer.query.filter_by(PhoneNumber=phone_number).all()
    # Trả về trang HTML với thông tin khách hàng nếu tìm thấy
    if customer:
        return render_template("user_list.html", customers=customer)
    else:
        return "<h3>Không tìm thấy khách hàng với thông tin đã nhập.</h3>", 404


def process_transfer():
    if request.method == "POST":
        pin = request.form["pin"]
        account_id = session.get("account_id")
        account = Account.query.get(account_id)
        # Kiểm tra mã PIN
        if not check_password_hash(account.PinCode, pin):
            flash("Mã pin không chính xác")
            return render_template("enter_pin.html")

            # Lấy thông tin người nhận
        recipient_account_number = session.get("recipient_account")
        recipient_account = Account.query.filter_by(
            accountNumber=recipient_account_number
        ).first()
        amount = Decimal((session.get("amount")))
        points_earned = int(amount // 1000)
        account.creditScore += points_earned

        # Tạo giao dịch
        transaction = Transaction(
            TransactionID=str(uuid.uuid4()),  # Tạo mã giao dịch duy nhất
            senderAccountNumber=account.accountNumber,
            recipientAccountNumber=recipient_account.accountNumber,
            TransactionDate=datetime.now(),
            TransactionType="Chuyển khoản nhanh",  # Chuyển khoản
            Amount=amount,
            Description=session.get("content"),
        )
        # Lưu giao dịch vào database
        db.session.add(transaction)

        # Cập nhật số dư tài khoản

        account.Balance -= amount
        recipient_account.Balance += amount
        db.session.commit()
        recipient_name = f"{recipient_account.customer.FirstName} {recipient_account.customer.LastName}"
        # Lấy thông tin chi tiết giao dịch để gửi email
        transaction_details = {
            "recipient_name": recipient_name,  # Tên người nhận từ bảng Customer
            "recipient_account": recipient_account.accountNumber,
            "amount": amount,
            "content": session.get("content"),
            "transaction_date": transaction.TransactionDate.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

        # Gửi email thông báo giao dịch
        send_transaction_email(account.Email, transaction_details)
        flash("Chuyển khoản thành công và email thông báo đã được gửi.", "success")
        return render_template("receipt.html", transaction=transaction_details)

    return render_template("enter_pin.html")


# Kiểm tra và khởi tạo chuyển khoản
def initiate_transfer():
    if request.method == "POST":
        recipient_account = request.form["recipient_account"]
        amount_str = request.form["amount"]
        amount = Decimal(amount_str)
        content = request.form["content"]
        account_id = session.get("account_id")
        # Kiểm tra thông tin chuyển khoản
        if not recipient_account or not amount or not content:
            flash("Vui lòng nhập đầy đủ thông tin ", "danger")

        account_receipt = Account.query.get(recipient_account)
        account_send = Account.query.get(account_id)
        if not account_receipt:
            flash("Tài khoản người nhận không tồn tại!")
            return redirect(url_for("transfer"))
        if account_send.balance < amount:
            flash("Số dư tài khoản không đủ để thực hiện giao dịch")
            return redirect(url_for("transfer"))
        # Lưu thông tin vào session cho bước xác nhận
        session["recipient_account"] = recipient_account
        session["amount"] = amount
        session["content"] = content

    return render_template("transfer_form.html")


def confirm_transaction():
    if request.method == "POST":
        return redirect(url_for("enter_pin"))

    recipient_account = session.get("recipient_account")
    amount = session.get("amount")
    content = session.get("content")
    return render_template(
        "confirm_transfer.html",
        recipient_account=recipient_account,
        amount=amount,
        content=content,
    )


def query_transaction():
    customer_id = session.get("customer_id")
    # Lấy ngày bắt đầu và ngày kết thúc
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    # Chuyển đổi chuỗi ngày tháng thành đối tượng datetime
    start_date = (
        datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    )
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    # Tìm giao dịch theo customer_id và lọc theo ngày (nếu có)
    query = Transaction.query.filter(
        or_(
            Transaction.senderAccountNumber == customer_id,
            Transaction.recipientAccountNumber == customer_id,
        )
    )

    if start_date and end_date:
        query = query.filter(
            Transaction.TransactionDate >= start_date,
            Transaction.TransactionDate <= end_date,
        )
    elif start_date:
        query = query.filter(Transaction.TransactionDate >= start_date)
    elif end_date:
        query = query.filter(Transaction.TransactionDate <= end_date)

    transactions = query.all()

    return render_template("transaction_history.html", transactions=transactions)


def process_withdrawal():
    if request.method == "POST":
        data = request.form  # Sử dụng request.form để nhận dữ liệu từ form POST
        pin = data.get("pin")
        amount = data.get("amount")
        account_id = session.get("account_id")
        if not account_id or not pin or not amount:
            return "Vui long nhập đủ thông tin", 400
        account = Account.query.get(account_id)
        # Kiểm tra mã PIN
        if not check_password_hash(account.PinCode, pin):
            flash("Mã pin không chính xác")
            return redirect(url_for("withdraw"))

        # Kiểm tra số dư tài khoản và số tiền rút
        amount = Decimal(amount)
        if amount < 100000:
            return {"success": False, "message": "Số tiền rút phải từ 100,000 VND."}
        if account.Balance >= amount:
            # Tạo bản ghi giao dịch
            transaction = Transaction(
                TransactionID=str(uuid.uuid4()),
                senderAccountNumber=account.accountNumber,
                recipientAccountNumber=None,
                TransactionDate=datetime.now(),
                TransactionType="Rút tiền",
                Amount=amount,
                Description="Rút tiền từ tài khoản",
            )

            # Lưu giao dịch và cập nhật số dư
            db.session.add(transaction)
            account.Balance -= amount
            db.session.commit()
            withdraw_name = f"{account.customer.FirstName} {account.customer.LastName}"
            transaction_details = {
                "withdrawer": withdraw_name,  # Tên người nhận từ bảng Customer
                "withdraw_account": account.accountNumber,
                "amount": amount,
                "transaction_date": transaction.TransactionDate.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
            send_withdraw_transaction_email(account.Email, transaction_details)

            flash("Rút tiền thành công! Vui lòng kiểm tra email")
            return render_template("receip_withdraw")
        else:
            flash("Số dư không đủ để rút!")
            return redirect(url_for("withdraw"))

    return render_template("withdraw.html")


def handle_login(username, password):

    account = Account.query.filter_by(Username=username).first()
    if not account:
        return "Tên đăng nhập không tồn tại", "danger", None
    attempts = session.get("login_attempts", 0)
    if attempts >= 5:
        return (
            "Tài khoản của bạn đã bị khóa do nhập sai quá nhiều lần. Vui lòng thử lại sau 15 phút",
            "warning",
            None,
        )

    # Kiểm tra password
    if not check_password_hash(account.Password, password):
        attempts += 1
        session["login_attempts"] = attempts  # Cập nhật số lần nhập sai trong session

        remaining_attempts = 5 - attempts
        if attempts >= 5:
            return (
                "Bạn đã nhập sai mật khẩu quá 5 lần. Tài khoản của bạn đã bị khóa trong 15 phút",
                "warning",
                None,
            )
        return (
            f"Mật khẩu không đúng. Bạn còn {remaining_attempts} lần thử.",
            "warning",
            None,
        )

    # Đăng nhập thành công
    session["login_attempts"] = 0
    return "Đăng nhập thành công!", "success", account.AccountID


def is_valid_email(email):
    email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


# Hàm kiểm tra username không chứa khoảng trắng
def is_valid_username(username):
    return " " not in username


# Hàm kiểm tra số điện thoại hợp lệ
def is_valid_phone_number(phone_number):
    phone_regex = r"^0\d{9}$"  # Bắt đầu bằng số 0 và có tổng cộng 10 chữ số
    return re.match(phone_regex, phone_number) is not None


def create_user_account():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"],
            "confirm_password": request.form["confirm_password"],
            "email": request.form["email"],
            "phone_number": request.form["phoneNumber"],
            "first_name": request.form["firstName"],
            "last_name": request.form["lastName"],
            "date_of_birth": datetime.strptime(
                request.form["dateOfBirth"], "%Y-%m-%d"
            ).date(),
            "address": request.form["address"],
            "city": request.form["city"],
            "country": request.form["country"],
        }
        # Kiểm tra định dạng email hợp lệ
        if not is_valid_email(data["email"]):
            flash("Email không hợp lệ!", "danger")
            return redirect(url_for("register"))  # Quay lại trang đăng ký

        # Kiểm tra username không có khoảng trắng
        if not is_valid_username(data["username"]):
            flash("Tên đăng nhập không hợp lệ!", "danger")
            return redirect(url_for("register"))

        # Kiểm tra số điện thoại hợp lệ
        if not is_valid_phone_number(data["phone_number"]):
            flash("Số điện thoại không hợp lệ!", "danger")
            return redirect(url_for("register"))
        # Kiểm tra username và email có tồn tại không
        existing_account = Account.query.filter_by(Username=data["username"]).first()
        existing_customer = Customer.query.filter_by(Email=data["email"]).first()
        if existing_account:
            return False, "Tài khoản đã tồn tại!"
        elif existing_customer:
            return False, "Email đã tồn tại!"

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(data["password"])

        # Tạo bản ghi Customer và Account
        new_customer = Customer(
            CustomerID=str(uuid.uuid4()),
            FirstName=data["first_name"],
            LastName=data["last_name"],
            DateOfBirth=data["date_of_birth"],
            Role="User",
            Email=data["email"],
            PhoneNumber=data["phone_number"],
            Address=data["address"],
            City=data["city"],
            Country=data["country"],
        )

        new_account = Account(
            AccountID=str(uuid.uuid4()),
            CustomerID=new_customer.CustomerID,
            Username=data["username"],
            Password=hashed_password,
            Email=data["email"],
            AccountType="savings",
            creditScored=0,
            DateOpened=datetime.date.today(),
            Status="Active",
        )

        # Thêm vào cơ sở dữ liệu
        db.session.add(new_customer)
        db.session.add(new_account)
        db.session.commit()
        session["new_account"] = {
            "AccountID": new_account.AccountID,
            "CustomerID": new_customer.CustomerID,
            "Username": new_account.Username,
            "Email": new_account.Email,
            "PhoneNumber": new_customer.PhoneNumber,
        }
        flash("Đăng ký thành công!")
        return redirect("/choose_account_number")

    return render_template("register.html")


def dashboard():
    total_transactions = Transaction.query.count()
    total_customers = Customer.query.count()
    total_money = db.session.query(db.func.sum(Account.Balance)).scalar()
    total_money = total_money // 24000 if total_money else 0

    latest_transactions = (
        db.session.query(Transaction, Account.Username)
        .join(Account, Transaction.senderAccountNumber == Account.AccountID)
        .order_by(Transaction.TransactionDate.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/admin.html",
        total_transactions=total_transactions,
        total_customers=total_customers,
        total_money=total_money,
        latest_transactions=latest_transactions,
    )


def retrieve_user():
    page = request.args.get("page", 1, type=int)  # Default to page 1
    per_page = 8  # 8 users per page

    pagination = (
        db.session.query(Customer)  # Lấy tất cả các trường từ bảng Customer
        .join(Account, Customer.CustomerID == Account.CustomerID)
        .add_columns(Account.Status)  # Thêm trường Status từ bảng Account
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    users = pagination.items

    return render_template("admin/user/user.html", users=users, pagination=pagination)


def update_user(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return "Khong tim thay khach hang", 404
    if request.method == "POST":
        # Lấy dữ liệu từ biểu mẫu để cập nhật
        customer.FirstName = request.form["FirstName"]
        customer.LastName = request.form["LastName"]
        customer.DateOfBirth = request.form.get("DateOfBirth")
        customer.Role = request.form["Role"]
        customer.Email = request.form["Email"]
        customer.PhoneNumber = request.form["PhoneNumber"]
        customer.Address = request.form["Address"]
        customer.City = request.form.get("City")
        customer.Country = request.form.get("Country")
        customer.Notes = request.form.get("Notes")

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return redirect(url_for("admin.user_list"))

    return render_template("admin/user/edit.html", user=customer)


def locked_user(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return "Khong tim thay khach hang", 404
    account = Account.query.filter_by(CustomerID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404
    # Cập nhật trạng thái tài khoản thành 'Locked'
    account.Status = "Locked"
    db.session.commit()
    return redirect(url_for("admin.user_list"))


def unlocked_user(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return "User not found", 404
    account = Account.query.filter_by(CustomerID=customer.CustomerID).first()
    if not account:
        return "Account not found", 404

    # Cập nhật trạng thái tài khoản thành 'Active'
    account.Status = "Active"
    db.session.commit()
    return redirect(url_for("admin.user_list"))


def get_transaction():
    page = request.args.get("page", 1, type=int)  # Default to page 1
    per_page = 6  # 6 transactions per page

    pagination = (
        db.session.query(Transaction)
        .order_by(Transaction.TransactionDate.desc())  # Sort newest to oldest
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    transactions = pagination.items

    return render_template(
        "admin/transaction/transaction.html",
        transactions=transactions,
        pagination=pagination,
    )
