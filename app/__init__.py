from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes.home_route import home_bp
from .routes.login_route import login_bp
from .routes.register_route import register_bp
from .routes.admin_route import admin_bp

# Khởi tạo SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Khởi động database
    db.init_app(app)

    # Đăng ký các blueprint

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(admin_bp)

    # Tạo bảng trong database (nếu chưa có)
    with app.app_context():
        db.create_all()

    return app
