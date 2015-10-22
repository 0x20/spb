# -- TRANSACTIONS : retrieve bank transactions

import logging
from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from app_code.banktransactions.BankTransactionDataStore import BankTransactionDataStore

storage = BankTransactionDataStore()
logger = logging.getLogger('transactions_api')

transactions_module = Blueprint('transactions', __name__)

# - retrieve bank transactions
@transactions_module.route("/brain/banktransactions/from/<string:from_ts>/to/<string:to_ts>", methods=['GET'])
def get_transactions(from_ts, to_ts):
    if ((to_ts == "undefined") or (to_ts == "")):
        to_ts = datetime.now().strftime("%Y-%m-%d")
    if ((from_ts == "undefined") or (from_ts == "")):
        from_ts = (datetime.now()-timedelta(weeks=1)).strftime("%Y-%m-%d")
    return jsonify({'transactions': storage.get_transactions(from_ts, to_ts)})

