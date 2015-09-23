#!bin/python
import sys
import logging
import logging.handlers
import ConfigParser

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app_code.ui import load_groundcontrol
from app_code.access.Access_api import access_module
from app_code.logs.Log_api import log_module
from app_code.miscellaneous.Login_api import login_module
from app_code.banktransactions.BankTransactions_api import transactions_module
from app_code.users.Users_api import users_module
from app_code.stock.Stock_api import stock_module
#from app_code.miscellaneous.payment_api import payment_module
from app_code.banktransactions import BankTransactionLoader


# The application consists of 2 parts:
# - a REST API
# - a web application that relies on (part of) the REST API for getting/manipulating data
# Flask is set up to serve both:
# - the web app (called 'groundcontrol') is HTML/AngularJS, and all files are served as static
#   files; 'groundcontrol' is configured as Flask's static folder
# - the REST API is dynamic
app = Flask(__name__, static_folder='../groundcontrol', static_url_path='')

logger = logging.getLogger('brainapi')

# Attach Flask blueprints for Brain API modules
app.register_blueprint(access_module)
app.register_blueprint(log_module)
app.register_blueprint(login_module)
app.register_blueprint(transactions_module)
app.register_blueprint(users_module)
app.register_blueprint(stock_module)
#app.register_blueprint(payment_module)
# Attach Flask blueprint that loads static GroundControl UI app files
app.register_blueprint(load_groundcontrol.groundcontrol_app)

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


