from flask import Blueprint, render_template

login_bp = Blueprint("login", __name__)


@login_bp.route("/login")
def home():
    return render_template("login.html")


@login_bp.route("/login/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")
