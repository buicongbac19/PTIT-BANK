from app.services.user_service import (
    get_list_user,
    handle_create_user,
    change_status_account,
    update_user,
    locked_user,
    unlocked_user,
    search_user,
    handle_login,
    initiate_transfer,
    confirm_transaction,
    process_transfer,
    query_transaction,
    process_withdrawal,
    create_user_account,
)

from flask import request, flash, redirect, url_for, session, render_template
import uuid


def get_list_user():
    return get_list_user()


def create_user():
    if request.method == "POST":
        data = {
            "customer_id": str(uuid.uuid4()),
            "first_name": request.form["FirstName"],
            "last_name": request.form["LastName"],
            "date_of_birth": request.form.get("DateOfBirth"),
            "role": "user",
            "email": request.form["Email"],
            "phone_number": request.form["PhoneNumber"],
            "address": request.form.get("Address"),
            "city": request.form.get("City"),
            "country": request.form.get("Country"),
            "notes": request.form.get("Notes"),
        }
        message, category, customer_id = handle_create_user(data)
        if category == "danger":
            flash(message, category)
            return render_template("register.html")
        else:
            flash("")
            return redirect(url_for("auth.create_account", customer_id=customer_id))
    return render_template("register.html")


def change_status_account(customer_id):
    return change_status_account(customer_id)


def update_user(customer_id):
    return update_user(customer_id)


def locked_user(customer_id):
    return locked_user(customer_id)


def unlocked_user(customer_id):
    return unlocked_user(customer_id)


def search_user():
    return search_user()


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        message, category, account_id = handle_login(username, password)
        if category == "danger":
            flash(message, category)
            return redirect(url_for("auth.login"))
        elif category == "warning":
            return render_template("login.html", is_open_popup=True, message=message)
        else:
            session["account_id"] = account_id
            flash("")
            return redirect(url_for("home.home"))
    return render_template("login.html", is_open_popup=False)


def start_transfer():
    return initiate_transfer()


def confirm_transaction():
    return confirm_transaction()


# Controller để xử lý giao dịch và kiểm tra mã PIN
def execute_transfer():
    return process_transfer()


def get_transaction():
    return query_transaction()


def handle_withdraw_request():
    return process_withdrawal()


def register_user():
    create_user_account()
