from flask import request, render_template_string, render_template, redirect, url_for, jsonify, flash

from app import app, db
from app.controllers.CRUDuser_controller import retrieving_user_controller, add_user_controller, \
    change_status_account_controller, updating_user_controller, locked_user_controller, unlocked_user_controller, \
    locking_for_user_controller

from app.models import Customer, Account


#Lấy về danh sách người dùng
@app.route('/customers')
def user_list():
    return retrieving_user_controller()


#Tạo người dùng mới
@app.route('/customers/create', methods=['POST'])
def create_user():
    return add_user_controller()


#Cập nhật trạng thái tài khoản của người dùng
@app.route('/customers/status/<customer_id>', methods=['POST'])
def update_account_status(customer_id):
    return change_status_account_controller(customer_id)


#Cập nhật thông tin người dùng
@app.route('/customers/update/<string:customer_id>', methods=['POST'])
def update_user(customer_id):
    return updating_user_controller(customer_id)


#Khóa người dùng
@app.route('/customers/lock/<string:customer_id>', methods=['POST'])
def lock_customer(customer_id):
    return locked_user_controller(customer_id)


#Mở khóa người dùng
@app.route('/customers/active/<string:customer_id>', methods=['POST'])
def active_user(customer_id):
    return unlocked_user_controller(customer_id)


#Tìm kiếm người dùng
@app.route('/customers/search', methods=['GET'])
def search_user():
    return locking_for_user_controller()
