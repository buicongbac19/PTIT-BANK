from flask import request, flash, url_for, render_template, redirect

from app.services.forgotPass_service import forgot_password_service, reset_password_service


def forgot_password_controller():
    if request.method == 'POST':
        email = request.form['email']
        result = forgot_password_service(email)
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('reset_password'))
        else:
            flash(result['message'], "danger")

    return render_template('forgot_password.html')


# Controller reset mật khẩu
def reset_password_controller():
    if request.method == 'POST':
        verification_code = request.form['verification_code']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Mật khẩu mới và mật khẩu nhập lại không khớp.", "danger")
            return render_template('reset_password.html')

        result = reset_password_service(verification_code, new_password)
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('login'))
        else:
            flash(result['message'], "danger")

    return render_template('reset_password.html')

