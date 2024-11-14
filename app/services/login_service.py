from flask import request, flash, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash

from app.models import Account


def login_service():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kiểm tra username
        account = Account.query.filter_by(username=username).first()
        if not account:
            flash("Tên đăng nhập không tồn tại", "danger")
            return render_template('login.html')
        # Kiểm tra password
        if not check_password_hash(account.password, password):
            flash("Mật khẩu không đúng", "danger")
            return render_template('login.html')

        # Đăng nhập thành công
        session['account_id'] = account.accountID
        flash("Đăng nhập thành công!", "success")
        return redirect(url_for('dashboard'))

    return render_template('login.html')

