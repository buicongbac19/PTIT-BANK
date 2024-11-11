from werkzeug.security import check_password_hash

from app.models import Account


def login_service(username, password):
    account = Account.query.filter_by(Username=username).first()
    if account and check_password_hash(account.Password, password):
        return {'success': True, 'account_id': account.AccountID}
    return {'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu không đúng'}
