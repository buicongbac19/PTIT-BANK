# routes/auth_routes.py
from flask import render_template, request, redirect, url_for
from app.controllers.auth_controller import register_user
from app import app


@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_user()
