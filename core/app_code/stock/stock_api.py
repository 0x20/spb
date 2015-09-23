
import logging
from flask import Blueprint, jsonify
from app_code.stock.StockDataStore import StockDataStore

storage = StockDataStore()
logger = logging.getLogger('stock_api')

stock_module = Blueprint('stock', __name__)

# -- Stock management

# - list of products currently offered
@stock_module.route('/brain/stock/products/all', methods=['GET'])
def get_all_products():
    logger.info("** Returning list of current products")
    return '\n'.join(storage.getproducts())

