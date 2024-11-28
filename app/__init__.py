from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Khởi động database
    db.init_app(app)

    # Import và đăng ký các blueprint
    from .routes.home_route import home_bp

    from .routes.admin_route import admin_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)

    # Tạo bảng trong database (nếu chưa có)
    with app.app_context():
        db.create_all()

    return app
