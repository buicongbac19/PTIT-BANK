from app import app
from app.controllers.transaction_history_controller import get_transaction


@app.route('/transactions/history', methods=['GET'])
def transaction_history():
    return get_transaction()


