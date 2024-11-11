from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Trang admin

@admin_bp.route('/')
def admin():
    return render_template('admin/admin.html')

# Quản lý tài khoản

@admin_bp.route('/account')
def account():
    return render_template('admin/account/account.html')

@admin_bp.route('/account/create')
def add_account():
    return render_template('admin/account/create.html')

@admin_bp.route('/account/edit')
def edit_account():
    return render_template('admin/account/edit.html')

# Nạp tiền vào tài khoản

@admin_bp.route('/account/recharge')
def recharge_account():
    return render_template('admin/account/recharge.html')

# Quản lý người dùng

@admin_bp.route('/user')
def user():
    return render_template('admin/user/user.html')

@admin_bp.route('/user/create') 
def add_user():
    return render_template('admin/user/create.html')

@admin_bp.route('/user/edit')
def edit_user():
    return render_template('admin/user/edit.html')

# Quản lý giao dịch

@admin_bp.route('/transaction')
def transaction():
    return render_template('admin/transaction/transaction.html')