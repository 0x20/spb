#!bin/python
import sys
import urllib
from datetime import datetime, timedelta
import logging
import logging.handlers
import ConfigParser

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from ui import load_groundcontrol

from application_code.util import returns_text
from application_code import PGDataStorage, BankTransactionLoader


# The application consists of 2 parts:
# - a REST API
# - a web application that relies on (part of) the REST API for getting/manipulating data
# Flask is set up to serve both:
# - the web app (called 'groundcontrol') is HTML/AngularJS, and all files are served as static
#   files; 'groundcontrol' is configured as Flask's static folder
# - the REST API is dynamic
app = Flask(__name__, static_folder='../groundcontrol', static_url_path='')
storage = PGDataStorage.PGDataStore()
logger = logging.getLogger('brainapi')


app.register_blueprint(load_groundcontrol.groundcontrol_app)

# BRAIN API

# -- ACCESS : methods for use by Gatekeeper and Dooropener

# - list of GSM numbers that are allowed to use Gatekeeper
@app.route('/brain/access/gsmnumbers/all', methods=['GET'])
@returns_text
def get_all_gsmnumbers():
    logger.info("** Returning list of GSM numbers")
    return '\n'.join(storage.getgsmnumbers())

# - list of GSM numbers that are allowed to use Gatekeeper
@app.route('/brain/access/schedules/all', methods=['GET'])
def get_all_schedules():
    logger.info("** Returning list of gatekeeper schedules")
    return jsonify({'schedules': storage.get_gatekeeper_schedules()})


@app.route('/brain/access/schedules/delete/<int:id>')
def delete_schedule(id):
    storage.delete_schedule(id)
    return "True"


@app.route('/brain/access/schedules/add/<string:day>/<string:from_ts>/<string:to_ts>')
def add_schedule(day, from_ts, to_ts):
    storage.add_schedule(day, from_ts, to_ts)
    return "True"



@app.route('/brain/access/whitelistfile', methods=['GET'])
@returns_text
def get_whitelist():
    logger.info("** Returning gatekeeper whitelist")
    return '\n'.join(storage.get_gatekeeper_whitelist())


# - list of badges that are allowed to use open the Space door
@app.route('/brain/access/badgenumbers/all', methods=['GET'])
def get_all_badgenumbers():
    logger.info("** Returning list of badge numbers")
    return '\n'.join(storage.getbadgenumbers())


# -- LOGS : retrieve the logs

# - retrieve the logs
@app.route("/brain/logs/from/<string:from_ts>/to/<string:to_ts>", methods=['GET'])
def get_logs(from_ts, to_ts):
    if ((to_ts == "undefined") or (to_ts == "")):
        to_ts = datetime.now().strftime("%Y-%m-%d")
    if ((from_ts == "undefined") or (from_ts == "")):
        from_ts = (datetime.now()-timedelta(weeks=1)).strftime("%Y-%m-%d")
    return jsonify({'logEntries': storage.get_logs(from_ts, to_ts)})


# - add a log entry:
@app.route('/brain/logs/add/<string:system>/<string:attribute>/<string:message>', methods=['GET'])
def store_log(system, attribute, message):
    storage.addlog(system, attribute, message)
    return "True"


# -- TRANSACTIONS : retrieve bank transactions

# - retrieve bank transactions
@app.route("/brain/banktransactions/from/<string:from_ts>/to/<string:to_ts>", methods=['GET'])
def get_transactions(from_ts, to_ts):
    if ((to_ts == "undefined") or (to_ts == "")):
        to_ts = datetime.now().strftime("%Y-%m-%d")
    if ((from_ts == "undefined") or (from_ts == "")):
        from_ts = (datetime.now()-timedelta(weeks=1)).strftime("%Y-%m-%d")
    return jsonify({'transactions': storage.get_transactions(from_ts, to_ts)})

# -- PAYMENT : Manages payments from users

# - add a banknote and process member payments
@app.route("/brain/payments/addbanknote")
def addbanknote():
    print "woah"
    pass

# -- USER : methods for user management

# - retrieve the list of users
@app.route('/brain/user/all', methods=['GET'])
def get_all_users():
    print "** all users' data"
    return jsonify({'users': storage.getusers()})

# - list of phone numbers for a user
@app.route('/brain/user/<string:user_id>/phonenumbers', methods=['GET'])
def get_phonenumbers_for_user(user_id):
    logger.info("** Returning list of phone numbers for user: %s", user_id)
    return jsonify({'phonenumbers': storage.getphonenumbers(user_id)})

# - update an existing user
@app.route('/brain/user/update/<string:id>/<string:firstname>/<string:lastname>/<any(true,false):member>', methods=['GET'])
def update_user(id, firstname, lastname, member):
    print "** update user data for: ", firstname, " ", lastname
    storage.updateuser(id, urllib.unquote(firstname), urllib.unquote(lastname), member)
    return "True"

# - update an existing user
@app.route('/brain/user/delete/<string:id>', methods=['GET'])
def delete_user(id):
    print "** delete user data for user ", id
    storage.deleteuser(id)
    return "True"

# - update a phone number
@app.route('/brain/user/updatephonenumber/<string:id>/<string:user_id>/<string:phonenumber>/<any(true,false):cellphone>', methods=['GET'])
def update_user_phonenumber(id, user_id, phonenumber, cellphone):
    print "** update phone number for: ", user_id
    storage.updatephonenumber(id, user_id, urllib.unquote(phonenumber), cellphone)
    return "True"

# - delete a phone number
@app.route('/brain/user/deletephonenumber/<int:id>', methods=['GET'])
def delete_phonenumber(id):
    print "** delete phone number ", id
    storage.deletephonenumber(id)
    return "True"

# - set a password
@app.route('/brain/user/<int:id>/updatepassword/<string:username>/<string:password>', methods=['GET'])
def set_usernamepassword(id, username, password):
    print "** set username/password for user ", id
    storage.setusernamepassword(id, username, password)
    return "True"

# - check a password
@app.route('/brain/login/<string:username>/<string:password>', methods=['GET'])
def check_password(username, password):
    print "** check username/password for user ", username
    if (storage.login(username, password)):
        return "True"
    else:
        return "False"

# -- Stock management

# - list of products currently offered
@app.route('/brain/stock/products/all', methods=['GET'])
def get_all_products():
    logger.info("** Returning list of current products")
    return '\n'.join(storage.getproducts())





if __name__ == '__main__':
    rootLogger = logging.getLogger()
    rootLogger.setLevel(level=logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    rootLogger.addHandler(ch)

    config = ConfigParser.ConfigParser()
    config.read("main.ini")

    # monitor a directory to import CSV bank transaction dump files
    bt_loader = BankTransactionLoader.BankTransactionLoader(config.get('BankTransactions', 'csvpath'), config.get('BankTransactions', 'csvarchivepath'))
    scheduler = BackgroundScheduler()
    bank_job = scheduler.add_job(bt_loader.check_files, 'interval', seconds=15)
    scheduler.start()
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARN)


    # using the reloader will cause apscheduler to run twice each time the interval elapses
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=config.getint('Host', 'port'))


