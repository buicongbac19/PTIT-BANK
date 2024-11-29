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


@home_bp.route("/account/credit-score")
def credit_score():
    return render_template("credit_score.html")


@home_bp.route("/account/settings")
def settings():
    return render_template("settings.html")
