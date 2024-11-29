from app.services.account_service import (
    retrieve_account,
    handle_create_account,
    locked_account,
    edit_account,
    unlocked_account,
    search_account,
    set_account_number,
    generate_account_numbers,
    handle_forgot_password,
    handle_reset_password,
    add_pin,
    update_pin,
    handle_verify_pin,
    handle_send_change_email_pin,
    handle_change_email,
    handle_send_change_password_pin,
    handle_change_password,
)


from flask import session, redirect, request, flash, render_template, url_for
from datetime import date
import uuid


def retrieve_account():
    return retrieve_account()


def create_account():
    customer_id = request.args.get("customer_id")
    if request.method == "POST":
        customer_id = request.form["CustomerID"]
        account_data = {
            "AccountID": str(uuid.uuid4()),
            "Username": request.form["Username"],
            "Password": request.form["Password"],
            "AccountType": request.form.get("AccountType", "standard"),
            "Balance": request.form.get("Balance", 50000),
            "Status": request.form.get("Status", "active"),
            "PinCode": request.form.get("PinCode", None),
            "creditScored": request.form.get("creditScored", 0),
            "CustomerID": customer_id,
            "DateOpened": date.today(),
        }
        message, category = handle_create_account(account_data)
        if category == "danger":
            flash(message, category)
            return render_template("create_account.html", customer_id=customer_id)
        else:
            flash("")
            return redirect(url_for("auth.login"))
    return render_template("create_account.html", customer_id=customer_id)


def edit_account(account_id):
    return edit_account()


def looked_account(account_id):
    return locked_account(account_id)


def unlooked_account(account_id):
    return unlocked_account(account_id)


def search_account():
    return search_account()


def handle_choose_account_number(account_number):
    return set_account_number(account_number)


# Xử lý tạo danh sách số tài khoản cho trang lựa chọn
def get_available_account_numbers():
    phone_number = session["new_account"]["PhoneNumber"]
    return generate_account_numbers(phone_number)


def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        data = {"email": email}
        message, category = handle_forgot_password(data)
        if category == "danger":
            flash(message, category)
            return render_template("forgot_password.html")
        else:
            return render_template("verify_code.html")
    return render_template("forgot_password.html")


def verify_code():
    if request.method == "POST":
        verify_code = request.form.get("verify_code")
        message, category = handle_verify_pin(verify_code)
        if category == "danger":
            flash(message, category)
            return render_template("verify_code.html")
        else:
            session.pop("verification_code", None)
            return render_template("reset_password.html")
    return render_template("verify_code.html")


# Controller reset mật khẩu
def reset_password():
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["repeat_password"]
        message, category = handle_reset_password(new_password, confirm_password)
        if category == "danger":
            flash(message, category)
            return render_template("reset_password.html")
        else:
            return redirect(url_for("auth.login"))
    return render_template("reset_password.html")


def send_change_email_pin():
    if request.method == "POST":
        email = request.form["email"]
        message, category = handle_send_change_email_pin(email)
        if category == "danger":
            flash(message, category)
            return redirect(url_for("auth.login"))
    return render_template("change_email.html")


def change_email():
    if request.method == "POST":
        new_email = request.form["new_email"]
        pin_code = request.form["verification_code"]
        message, category = handle_change_email(new_email, pin_code)
        if category == "danger":
            flash(message, category)
            return redirect(url_for("home.change_email"))
        else:
            return redirect(url_for("home.settings"))
    return render_template("change_email.html")


def send_change_password_pin():
    if request.method == "POST":
        email = request.form["email"]
        message, category = handle_send_change_password_pin(email)
        if category == "danger":
            flash(message, category)
            return redirect(url_for("auth.login"))
    return render_template("change_password.html")


def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        pin_code = request.form["verification_code"]
        message, category = handle_change_password(old_password, new_password, pin_code)
        if category == "danger":
            flash(message, category)
            return redirect(url_for("home.change_password"))
        else:
            return redirect(url_for("home.settings"))
    return render_template("change_password.html")


def add_pin():
    return add_pin()


# Controller để xử lý form đổi mã PIN
def update_pin():
    return update_pin()