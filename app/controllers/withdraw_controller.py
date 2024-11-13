from flask import request, jsonify, session, render_template

from app.models import Account
from app.services.withdraw_service import process_withdrawal


def handle_withdraw_request():
    return process_withdrawal()
