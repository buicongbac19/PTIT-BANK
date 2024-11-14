from flask import request, session, redirect, url_for, flash, render_template
from app.services.pinCode_service import add_pin_service, update_pin_service


# Controller để xử lý form thêm mã PIN
def add_pin_controller():
    return add_pin_service()


# Controller để xử lý form đổi mã PIN
def update_pin_controller():
    return update_pin_service()
