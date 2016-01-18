# -- FLAPPERS : submit text to the flappers

import logging
import ConfigParser
from time import sleep
from flask import Blueprint, jsonify
from netcat import Netcat

logger = logging.getLogger('flappers_api')

flappers_module = Blueprint('flappers', __name__)

config = ConfigParser.ConfigParser()
config.read("main.ini")
flappers_host = config.get("Flappers", "host")
flappers_port = config.getint("Flappers", "port")

# - Show message on the flappers
@flappers_module.route('/brain/flappers/msg/<string:text>', methods=['GET'])
def send_to_flappers(text):
    txt = text[:4]
    print "** send to flappers ", txt
    nc = Netcat(flappers_host, flappers_port)
    nc.write(txt + '\n')
    sleep(10)
    nc.write('@@@@\n')
    nc.close()
    return "True"


# - Show message on the flappers
@flappers_module.route('/brain/flappers/calibrate/<string:text>', methods=['GET'])
def calibrate_flappers(text):
    txt = text[:4]
    print "** calibrate flappers ", txt
    nc = Netcat(flappers_host, flappers_port)
    nc.write('$iread ' + txt + '\n')
    nc.close()
    return "True"

