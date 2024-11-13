from app.services.sendEmail_service import send_verification_email_service, send_transaction_email_service, \
    send_withdrawtransaction_email_service


def send_verification_email(email, verification_code):
    return send_verification_email_service(email, verification_code)


def send_transaction_email(user_email, transaction_details):
    return send_transaction_email_service(user_email, transaction_details)


def send_withdrawtransaction_email(user_email, transaction_details):
    return send_withdrawtransaction_email_service(user_email, transaction_details)
