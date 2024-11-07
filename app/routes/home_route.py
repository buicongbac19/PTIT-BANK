from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return render_template("home.html")


@home_bp.route("/account/profile")
def profile():
    return render_template("profile.html")


@home_bp.route("/account/transfer-money")
def transfer_money():
    return render_template("transfer_money.html")
