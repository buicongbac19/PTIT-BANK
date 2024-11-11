# controllers/auth_controller.py
from datetime import datetime

from flask import render_template, request, redirect, flash
from app.services.auth_service import create_user_account


def register_user():
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

        # Gọi service để xử lý đăng ký người dùng
        success, message = create_user_account(data)

        if success:
            flash("Registration successful!")
            return redirect('/choose_account_number')
        else:
            flash(message)
            return redirect('/register')

    return render_template('register.html')
