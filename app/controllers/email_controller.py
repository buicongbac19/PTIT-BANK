from app.services.email_service import (
    send_verification_email_service,
    send_transaction_email,
    send_withdrawtransaction_email,
)


def send_verification_email(email, verification_code):
    return send_verification_email_service(email, verification_code)


def send_transaction_email(user_email, transaction_details):
    return send_transaction_email(user_email, transaction_details)


def send_withdrawtransaction_email(user_email, transaction_details):
    return send_withdrawtransaction_email(user_email, transaction_details)
