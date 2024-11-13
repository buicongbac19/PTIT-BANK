import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "hhtrinh2505@gmail.com"
SENDER_PASSWORD = "gslj zyxq baxt ekqg"


def setup_email_server():
    """Thiết lập kết nối đến máy chủ SMTP."""
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    return server


def create_email_message(subject, body, recipient_email):
    """Tạo đối tượng email với tiêu đề và nội dung."""
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    return message


def send_verification_email_service(email, verification_code):
    subject = "Mã xác thực đổi mật khẩu"
    body = f"Mã xác thực của bạn là: {verification_code}"

    # Tạo email và gửi
    message = create_email_message(subject, body, email)
    try:
        with setup_email_server() as server:
            server.sendmail(SENDER_EMAIL, email, message.as_string())
            print("Email mã xác thực đã được gửi thành công.")
    except Exception as e:
        print("Error sending verification email:", e)


def send_transaction_email_service(user_email, transaction_details):
    subject = "Thông báo giao dịch thành công"
    body = f"""Xin chào,

Giao dịch của bạn đã được thực hiện thành công.
Thông tin giao dịch:
- Người nhận: {transaction_details['recipient_name']}
- Số tài khoản người nhận: {transaction_details['recipient_account']}
- Số tiền: {transaction_details['amount']} VND
- Nội dung: {transaction_details['content']}
- Ngày giao dịch: {transaction_details['transaction_date']}

Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi.
"""

    # Tạo email và gửi
    message = create_email_message(subject, body, user_email)
    try:
        with setup_email_server() as server:
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
            print("Email thông báo giao dịch đã được gửi thành công.")
    except Exception as e:
        print("Không thể gửi email thông báo giao dịch. Lỗi:", e)


def send_withdrawtransaction_email_service(user_email, transaction_details):
    subject = "Thông báo giao dịch thành công"
    body = f"""Xin chào,

Giao dịch rút tiền của bạn đã được thực hiện thành công.
Thông tin giao dịch:
- Người rút: {transaction_details['withdrawer']}
- Số tài khoản người rút: {transaction_details['withdraw_account']}
- Số tiền: {transaction_details['amount']} VND
- Ngày giao dịch: {transaction_details['transaction_date']}

Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi.
"""

    # Tạo email và gửi
    message = create_email_message(subject, body, user_email)
    try:
        with setup_email_server() as server:
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
            print("Email thông báo giao dịch đã được gửi thành công.")
    except Exception as e:
        print("Không thể gửi email thông báo giao dịch. Lỗi:", e)

