#!bin/python

import sys
import logging
import logging.handlers
import ConfigParser

# the Flask framework is used to host the HTTP stuff:
# - static hosting of the UI (GroundControl: HTML+JS files)
# - the SmarterSpaceBrain REST API, which is used by GroundControl
from flask import Flask
# apscheduler is used to periodically run the bank transaction loader job
from apscheduler.schedulers.background import BackgroundScheduler

# Load all different modules
# Rest API modules are defined as Flask Blueprints. They are imported here,
# and hooked into the main Flask app below.
from app_code.ui import load_groundcontrol
from app_code.access.Access_api import access_module
from app_code.logs.Log_api import log_module
from app_code.users.Login_api import login_module
from app_code.banktransactions.BankTransactions_api import transactions_module
from app_code.users.Users_api import users_module
from app_code.stock.Stock_api import stock_module
#from app_code.miscellaneous.payment_api import payment_module
from app_code.banktransactions import BankTransactionLoader
from app_code.miscellaneous.Flappers_api import flappers_module

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# The application consists of 2 parts:
# - a REST API
# - a web application that relies on (part of) the REST API for getting/manipulating data
# Flask is set up to serve both:
# - the web app (called 'GroundControl') is HTML/AngularJS, and all files are served as static
#   files; 'groundcontrol' is configured as Flask's static folder. In principle, GroundControl
#   is fully separated from the REST api, but it is hosted by the same Flask app for 2 reasons:
#   (1) simplicity (one item to deploy and run) (2) JS rest calls have to go the same
#   host/port combination, otherwise browsers will complain because they suspect cross-site scripting
# - the REST API is dynamic
app = Flask(__name__, static_folder='../groundcontrol', static_url_path='')

logger = logging.getLogger('brainapi')

# Attach Flask blueprints for Brain API modules
app.register_blueprint(access_module)
app.register_blueprint(flappers_module)
app.register_blueprint(log_module)
app.register_blueprint(login_module)
app.register_blueprint(transactions_module)
app.register_blueprint(users_module)
app.register_blueprint(stock_module)
#app.register_blueprint(payment_module)
# Attach Flask blueprint that loads static GroundControl UI app files
app.register_blueprint(load_groundcontrol.groundcontrol_app)

# Set up the main application: logging, Flask app, and the banktransactions load job.
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


