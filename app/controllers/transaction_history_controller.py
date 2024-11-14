from datetime import datetime

from flask import session, request

from app.services.transaction_history_service import query_transaction


def get_transaction():
    return query_transaction()
