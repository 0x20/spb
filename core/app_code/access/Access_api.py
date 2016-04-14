# -- ACCESS : methods for use by Gatekeeper and Dooropener

import logging
from flask import Blueprint, jsonify
from app_code.util import returns_text
from AccessDataStore import AccessDataStore

storage = AccessDataStore()
logger = logging.getLogger('access_api')

access_module = Blueprint('access', __name__)


# - list of GSM numbers that are allowed to use Gatekeeper
@access_module.route('/brain/access/gsmnumbers/all', methods=['GET'])
@returns_text
def get_all_gsmnumbers():
    logger.info("** Returning list of GSM numbers")
    return '\n'.join(storage.getgsmnumbers())

# - list of GSM numbers that are allowed to use Gatekeeper
@access_module.route('/brain/access/schedules/all', methods=['GET'])
def get_all_schedules():
    logger.info("** Returning list of gatekeeper schedules")
    return jsonify({'schedules': storage.get_gatekeeper_schedules()})

@access_module.route('/brain/access/schedules/delete/<int:id>')
def delete_schedule(id):
    storage.delete_schedule(id)
    return "True"

@access_module.route('/brain/access/schedules/add/<string:day>/<string:from_ts>/<string:to_ts>')
def add_schedule(day, from_ts, to_ts):
    storage.add_schedule(day, from_ts, to_ts)
    return "True"

@access_module.route('/brain/access/whitelistfile', methods=['GET'])
@returns_text
def get_whitelist():
    logger.info("** Returning gatekeeper whitelist")
    return '\n'.join(storage.get_gatekeeper_whitelist())

# - list of badges that are allowed to use open the Space door
@access_module.route('/brain/access/badgenumbers/all', methods=['GET'])
@returns_text
def get_all_badgenumbers():
    logger.info("** Returning list of badge numbers")
    return '\n'.join(storage.getbadgenumbers())


