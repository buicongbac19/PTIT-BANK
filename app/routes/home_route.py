from flask import Blueprint, render_template
from app.controllers.home_controller import create_user

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    # Thêm một người dùng mẫu vào database
    create_user("JohnDoe", "john@example.com")
    return "User created!"
