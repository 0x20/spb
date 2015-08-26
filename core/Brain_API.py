#!/usr/bin/env python

import sys
import urllib
from datetime import datetime, timedelta
import logging
import logging.handlers
import ConfigParser

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from application_code.util import returns_text
from application_code.PGDataStorage import PGDataStore
from application_code.BankTransactionLoader import BankTransactionLoader


# The application consists of 2 parts:
# - a REST API
# - a web application that relies on (part of) the REST API for getting/manipulating data
# Flask is set up to serve both:
# - the web app (called 'groundcontrol') is HTML/AngularJS, and all files are served as static
#   files; 'groundcontrol' is configured as Flask's static folder
# - the REST API is dynamic
app = Flask(__name__, static_folder='../groundcontrol', static_url_path='')
storage = PGDataStore()
logger = logging.getLogger('brainapi')


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



# GROUNDCONTROL WEBAPP
# Serving static files; the client runs fully within the user's browser

@app.route('/groundcontrol')
def default():
    return groundcontrol()

@app.route('/groundcontrol/')
def default2():
    return groundcontrol()

@app.route('/groundcontrol/index.html')
def default_index():
    return groundcontrol()

@app.route('/groundcontrol/angular-1.3.15.min.js')
def angular():
    return app.send_static_file('angular-1.3.15.min.js')

@app.route('/groundcontrol/angular.min.js.map')
def angular_map():
    return app.send_static_file('angular.min.js.map')

@app.route('/groundcontrol/ngDialog.min.js')
def ngDialog_js():
    return app.send_static_file('ngDialog.min.js')

@app.route('/groundcontrol/ngDialog.min.css')
def ngDialog_css():
    return app.send_static_file('ngDialog.min.css')

@app.route('/groundcontrol/groundcontrol.html')
def groundcontrol():
    return app.send_static_file('groundcontrol.html')

@app.route('/groundcontrol/groundcontrol.js')
def groundcontrol_code():
    return app.send_static_file('groundcontrol.js')

@app.route('/groundcontrol/groundcontrol.css')
def groundcontrol_style():
    return app.send_static_file('groundcontrol.css')

@app.route('/groundcontrol/jquery-ui.min.css')
def groundcontrol_jquery_style():
    return app.send_static_file('jquery-ui.min.css')

@app.route('/groundcontrol/jquery-ui.min.js')
def groundcontrol_jquery_code():
    return app.send_static_file('jquery-ui.min.js')

@app.route('/groundcontrol/jquery-1.11.3.min.js')
def groundcontrol_jquery_min_code():
    return app.send_static_file('jquery-1.11.3.min.js')

@app.route('/groundcontrol/images/ui-bg_gloss-wave_35_8d8d8d_500x100.png')
def groundcontrol_jquery_image1():
    return app.send_static_file('images/ui-bg_gloss-wave_35_8d8d8d_500x100.png')

@app.route('/groundcontrol/images/ui-icons_ffffff_256x240.png')
def groundcontrol_jquery_image2():
    return app.send_static_file('images/ui-icons_ffffff_256x240.png')

@app.route('/groundcontrol/images/ui-bg_highlight-soft_75_5c635b_1x100.png')
def groundcontrol_jquery_image3():
    return app.send_static_file('images/ui-bg_highlight-soft_75_5c635b_1x100.png')

@app.route('/groundcontrol/images/ui-bg_glass_100_f6f6f6_1x400.png')
def groundcontrol_jquery_image4():
    return app.send_static_file('images/ui-bg_glass_100_f6f6f6_1x400.png')

@app.route('/groundcontrol/images/ui-icons_92908e_256x240.png')
def groundcontrol_jquery_image5():
    return app.send_static_file('images/ui-icons_92908e_256x240.png')

@app.route('/groundcontrol/images/ui-bg_glass_100_2f2f2e_1x400.png')
def groundcontrol_jquery_image6():
    return app.send_static_file('images/ui-bg_glass_100_2f2f2e_1x400.png')


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
    bt_loader = BankTransactionLoader(config.get('BankTransactions', 'csvpath'), config.get('BankTransactions', 'csvarchivepath'))
    scheduler = BackgroundScheduler()
    bank_job = scheduler.add_job(bt_loader.check_files, 'interval', seconds=15)
    scheduler.start()
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARN)


    # using the reloader will cause apscheduler to run twice each time the interval elapses
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=config.getint('Host', 'port'))


