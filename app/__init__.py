from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Khởi tạo đối tượng SQLAlchemy
app = Flask(__name__, template_folder='templates')

from .routes import auth_routes, forgotPass_routes, login_routes, choose_account_routes, home, dashboard, pinCode_routes, transaction_routes


app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ptit_database.db'  # Thay bằng kết nối cơ sở dữ liệu của bạn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Tùy chọn không cần thiết nhưng có thể giúp giảm overhead

db.init_app(app)

