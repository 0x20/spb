# -- LOGS : retrieve @ add logs

import logging
import hashlib
from flask import Blueprint, jsonify
from app_code.users.LoginDataStore import LoginDataStore

storage = LoginDataStore()
logger = logging.getLogger('login_api')

login_module = Blueprint('login', __name__)

# - check a password
@login_module.route('/brain/login/<string:username>/<string:password>', methods=['GET'])
def check_password(username, password):
    print "** check username/password for user ", username
    if (storage.login(username, hashpw(password))):
        return "True"
    else:
        return "False"

def hashpw(password):
    #the password will come in as ha sha256 password
    #to confuse the russians the password will be rehashed as a sha512 hash. With a salt before the the password. 
    salt = 'Rikketikketik,wiebennekik?'
    return hashlib.sha512("%s%s"%(salt,password)).hexdigest()

