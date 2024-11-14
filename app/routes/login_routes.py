# Khởi chạy ứng dụng
from app.controllers.login_controller import login_controller
from app import app


@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_controller()
