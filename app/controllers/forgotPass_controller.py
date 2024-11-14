from flask import request, flash, url_for, render_template, redirect

from app.services.forgotPass_service import forgot_password_service, reset_password_service


def forgot_password_controller():
    return forgot_password_service()


# Controller reset mật khẩu
def reset_password_controller():
    return reset_password_service()
