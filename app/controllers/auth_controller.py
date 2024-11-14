# controllers/auth_controller.py
from datetime import datetime

from flask import render_template, request, redirect, flash
from app.services.auth_service import create_user_account


def register_user():
    create_user_account()