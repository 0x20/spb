# -- FLAPPERS : submit text to the flappers

import logging
from time import sleep
from flask import Blueprint, jsonify
from netcat import Netcat

logger = logging.getLogger('flappers_api')

flappers_module = Blueprint('flappers', __name__)

# - Show message on the flappers
@flappers_module.route('/brain/flappers/msg/<string:text>', methods=['GET'])
def send_to_flappers(text):
    txt = text[:4]
    print "** send to flappers ", txt
    nc = Netcat('172.22.32.124', 1337)
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
    nc = Netcat('172.22.32.124', 1337)
    nc.write('$iread ' + txt + '\n')
    nc.close()
    return "True"

