# -- FLAPPERS : submit text to the flappers

import logging
from time import sleep
from flask import Blueprint, jsonify
from netcat import Netcat

logger = logging.getLogger('flappers_api')

flappers_module = Blueprint('flappers', __name__)

# - check a password
@flappers_module.route('/brain/flappers/<string:text>', methods=['GET'])
def send_to_flappers(text):
    txt = text[:4]
    print "** send to flappers ", txt
    nc = Netcat('172.22.32.124', 1337)
    nc.write(txt + '\n')
    sleep(10)
    nc.write('@@@@\n')
    nc.close()
    return "True"


