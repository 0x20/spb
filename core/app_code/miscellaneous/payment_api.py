
import logging
from flask import Blueprint, jsonify
from app_code.miscellaneous.PaymentDataStore import PaymentDataStore

storage = PaymentDataStore()
logger = logging.getLogger('payment_api')

payment_module = Blueprint('payment', __name__)


# -- PAYMENT : Manages payments from users

# - add a banknote and process member payments
@payment_module.route("/brain/payments/addbanknote")
def addbanknote():
    print "woah"
    pass


