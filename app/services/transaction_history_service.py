from datetime import datetime

from flask import request, session, render_template
from sqlalchemy import or_
from app.models import Transaction


def query_transaction():
    customer_id = session.get('customer_id')
    # Lấy ngày bắt đầu và ngày kết thúc
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Chuyển đổi chuỗi ngày tháng thành đối tượng datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    # Tìm giao dịch theo customer_id và lọc theo ngày (nếu có)
    query = Transaction.query.filter(
        or_(Transaction.senderAccountNumber == customer_id, Transaction.recipientAccountNumber == customer_id)
    )

    if start_date and end_date:
        query = query.filter(Transaction.TransactionDate >= start_date, Transaction.TransactionDate <= end_date)
    elif start_date:
        query = query.filter(Transaction.TransactionDate >= start_date)
    elif end_date:
        query = query.filter(Transaction.TransactionDate <= end_date)

    transactions = query.all()

    return render_template("transaction_history.html", transactions=transactions)
