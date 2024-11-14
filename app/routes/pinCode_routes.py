from flask import Blueprint
from app.controllers.pinCode_controller import add_pin_controller, update_pin_controller

from app import app


# Route để thiết lập mã PIN
@app.route('/addpin', methods=['POST', 'GET'])
def add_pin():
    return add_pin_controller()


# Route để cập nhật mã PIN
@app.route('/updatepin', methods=['POST', 'GET'])
def update_pin():
    return update_pin_controller()
