from flask import request, session, flash, render_template, redirect, url_for

from app.services.login_service import login_service


def login_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = login_service(username, password)
        if result['success']:
            session['account_id'] = result['account_id']
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('dashboard'))

        else:
            flash(result['message'], "danger")

    return render_template('login.html')
