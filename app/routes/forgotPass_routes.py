from app import app
from app.controllers.forgotPass_controller import forgot_password_controller, reset_password_controller


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return forgot_password_controller()


# Route reset mật khẩu
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return reset_password_controller()
