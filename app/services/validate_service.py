import re


def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


# Hàm kiểm tra username không chứa khoảng trắng
def is_valid_username(username):
    return " " not in username


# Hàm kiểm tra số điện thoại hợp lệ
def is_valid_phone_number(phone_number):
    phone_regex = r'^0\d{9}$'  # Bắt đầu bằng số 0 và có tổng cộng 10 chữ số
    return re.match(phone_regex, phone_number) is not None
