# -- LOGS : retrieve @ add logs

import logging
from flask import Blueprint, jsonify
from app_code.miscellaneous.LoginDataStore import LoginDataStore

storage = LoginDataStore()
logger = logging.getLogger('login_api')

login_module = Blueprint('login', __name__)

# - check a password
@login_module.route('/brain/login/<string:username>/<string:password>', methods=['GET'])
def check_password(username, password):
    print "** check username/password for user ", username
    if (storage.login(username, password)):
        return "True"
    else:
        return "False"


