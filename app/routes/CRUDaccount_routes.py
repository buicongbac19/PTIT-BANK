import string
import random

from flask import render_template, request, redirect, url_for
from wtforms.validators import length
from app.controllers.CRUDaccount_controller import retrieving, CreateAcc, EditingAcc, LockedAcc, SearchAcc
from app import app, db
from app.models import Account



#Lấy về danh sách tài khoản
@app.route('/accounts')
def account_list():
    return retrieving()


#Thêm tài khoản mới
@app.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    return CreateAcc()


#Update tài khoản
@app.route('/accounts/edit/<account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    return EditingAcc(account_id)


#Khóa tài khoản
@app.route('/accounts/lock/<account_id>', methods=['POST'])
def locked_account(account_id):
    return LockedAcc(account_id)


#Mở khóa tài khoản
@app.route('/account/active/<account_id>', methods=['POST'])
def active_account(account_id):
    return unlockedAcc(account_id)


#Tìm kiếm tài khoản
@app.route('/accounts/search', methods=['GET'])
def search_account():
    return SearchAcc()
