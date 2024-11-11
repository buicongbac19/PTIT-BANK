from flask import render_template, request, redirect, url_for
from app.controllers.auth_controller import register_user
from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello'
