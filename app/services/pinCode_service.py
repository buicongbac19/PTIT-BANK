import re
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Account  # Giả sử bạn có model Account đã được định nghĩa


# Service để thêm mã PIN mới
def add_pin_service(account_id, new_pin):
    if not new_pin:
        return {'success': False, 'message': 'Mã PIN không thể trống.'}
    # Kiểm tra độ dài mã PIN hợp lệ
    if not re.match(r"^\d{6}$", new_pin):
        return {'success': False, 'message': 'Mã PIN phải là 6 chữ số.'}

    account = Account.query.get(account_id)
    if account:
        if account.PinCode:
            return {'success': False, 'message': 'Mã PIN đã tồn tại. Hãy sử dụng chức năng cập nhật.'}

        account.PinCode = generate_password_hash(new_pin)
        db.session.commit()
        return {'success': True, 'message': 'Mã PIN đã được thêm thành công.'}
    return {'success': False, 'message': 'Tài khoản không tồn tại.'}


# Service để cập nhật mã PIN
def update_pin_service(account_id, old_pin, new_pin):
    if not re.match(r"^\d{6}$", new_pin):
        return {'success': False, 'message': 'Mã PIN mới phải là 6 chữ số.'}

    account = Account.query.get(account_id)
    if account:
        # Kiểm tra mã PIN cũ
        if not check_password_hash(account.PinCode, old_pin):
            return {'success': False, 'message': 'Mã PIN cũ không chính xác.'}

        account.PinCode = generate_password_hash(new_pin)
        db.session.commit()
        return {'success': True, 'message': 'Mã PIN đã được cập nhật thành công.'}
    return {'success': False, 'message': 'Tài khoản không tồn tại.'}
