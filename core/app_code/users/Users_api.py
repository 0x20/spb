# -- USER : methods for user management

import logging
import urllib
from flask import Blueprint, jsonify
from app_code.users.UsersDataStore import UsersDataStore
import hashlib

storage = UsersDataStore()
logger = logging.getLogger('users_api')

users_module = Blueprint('users', __name__)

# - retrieve the list of users
@users_module.route('/brain/user/all', methods=['GET'])
def get_all_users():
    print "** all users' data"
    return jsonify({'users': storage.getusers()})

# - list of phone numbers for a user
@users_module.route('/brain/user/<string:user_id>/phonenumbers', methods=['GET'])
def get_phonenumbers_for_user(user_id):
    logger.info("** Returning list of phone numbers for user: %s", user_id)
    return jsonify({'phonenumbers': storage.getphonenumbers(user_id)})

# - update an existing user
@users_module.route('/brain/user/update/<string:id>/<string:firstname>/<string:lastname>/<string:nickname>/<any(true,false):member>', methods=['GET'])
def update_user(id, firstname, lastname, nickname, member):
    print "** update user data for: ", firstname, " ", lastname, " (", nickname , ")"
    storage.updateuser(id, urllib.unquote(firstname), urllib.unquote(lastname), urllib.unquote(nickname), member)
    return "True"

# - update an existing user
@users_module.route('/brain/user/delete/<string:id>', methods=['GET'])
def delete_user(id):
    print "** delete user data for user ", id
    storage.deleteuser(id)
    return "True"

# - update a phone number
@users_module.route('/brain/user/updatephonenumber/<string:id>/<string:user_id>/<string:phonenumber>/<any(true,false):cellphone>', methods=['GET'])
def update_user_phonenumber(id, user_id, phonenumber, cellphone):
    print "** update phone number for: ", user_id
    storage.updatephonenumber(id, user_id, urllib.unquote(phonenumber), cellphone)
    return "True"

# - delete a phone number
@users_module.route('/brain/user/deletephonenumber/<int:id>', methods=['GET'])
def delete_phonenumber(id):
    print "** delete phone number ", id
    storage.deletephonenumber(id)
    return "True"

# - set a password
@users_module.route('/brain/user/<int:id>/updatepassword/<string:username>/<string:password>', methods=['GET'])
def set_usernamepassword(id, username, password):
    print "** set username/password for user ", id
    storage.setusernamepassword(id, username, hashpw(password))
    return "True"

def hashpw(password):
    #the password will come in as ha sha256 password
    #to confuse the russians the password will be rehashed as a sha512 hash. With a salt before the the password. 
    salt = 'Rikketikketik,wiebennekik?'
    return hashlib.sha512("%s%s"%(salt,password)).hexdigest()

