# -- LOGS : retrieve @ add logs

import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from app_code.database import PGDataStorage

storage = PGDataStorage.PGDataStore()
logger = logging.getLogger('log_api')

log_module = Blueprint('logs', __name__)

# - retrieve the logs
@log_module.route("/brain/logs/from/<string:from_ts>/to/<string:to_ts>", methods=['GET'])
def get_logs(from_ts, to_ts):
    if ((to_ts == "undefined") or (to_ts == "")):
        to_ts = datetime.now().strftime("%Y-%m-%d")
    if ((from_ts == "undefined") or (from_ts == "")):
        from_ts = (datetime.now()-timedelta(weeks=1)).strftime("%Y-%m-%d")
    return jsonify({'logEntries': storage.get_logs(from_ts, to_ts)})


# - add a log entry:
@log_module.route('/brain/logs/add/<string:system>/<string:attribute>/<string:message>', methods=['GET'])
def store_log(system, attribute, message):
    storage.addlog(system, attribute, message)
    return "True"


