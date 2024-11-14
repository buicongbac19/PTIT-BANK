
from app import app
from app.controllers.withdraw_controller import handle_withdraw_request


@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    return handle_withdraw_request()
