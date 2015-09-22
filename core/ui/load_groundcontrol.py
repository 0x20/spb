
from flask import Blueprint

groundcontrol_app = Blueprint('groundcontrol', __name__, static_folder='../../groundcontrol', static_url_path='')

# GROUNDCONTROL WEBAPP
# Serving static files; the client runs fully within the user's browser

@groundcontrol_app.route('/groundcontrol')
def default():
    return groundcontrol()

@groundcontrol_app.route('/groundcontrol/')
def default2():
    return groundcontrol()

@groundcontrol_app.route('/groundcontrol/index.html')
def default_index():
    return groundcontrol()

@groundcontrol_app.route('/groundcontrol/angular-1.3.15.min.js')
def angular():
    return groundcontrol_app.send_static_file('angular-1.3.15.min.js')

@groundcontrol_app.route('/groundcontrol/angular.min.js.map')
def angular_map():
    return groundcontrol_app.send_static_file('angular.min.js.map')

@groundcontrol_app.route('/groundcontrol/ngDialog.min.js')
def ngDialog_js():
    return groundcontrol_app.send_static_file('ngDialog.min.js')

@groundcontrol_app.route('/groundcontrol/ngDialog.min.css')
def ngDialog_css():
    return groundcontrol_app.send_static_file('ngDialog.min.css')

@groundcontrol_app.route('/groundcontrol/groundcontrol.html')
def groundcontrol():
    return groundcontrol_app.send_static_file('groundcontrol.html')

@groundcontrol_app.route('/groundcontrol/groundcontrol.js')
def groundcontrol_code():
    return groundcontrol_app.send_static_file('groundcontrol.js')

@groundcontrol_app.route('/groundcontrol/groundcontrol.css')
def groundcontrol_style():
    return groundcontrol_app.send_static_file('groundcontrol.css')

@groundcontrol_app.route('/groundcontrol/jquery-ui.min.css')
def groundcontrol_jquery_style():
    return groundcontrol_app.send_static_file('jquery-ui.min.css')

@groundcontrol_app.route('/groundcontrol/jquery-ui.min.js')
def groundcontrol_jquery_code():
    return groundcontrol_app.send_static_file('jquery-ui.min.js')

@groundcontrol_app.route('/groundcontrol/jquery-1.11.3.min.js')
def groundcontrol_jquery_min_code():
    return groundcontrol_app.send_static_file('jquery-1.11.3.min.js')

@groundcontrol_app.route('/groundcontrol/images/ui-bg_gloss-wave_35_8d8d8d_500x100.png')
def groundcontrol_jquery_image1():
    return groundcontrol_app.send_static_file('images/ui-bg_gloss-wave_35_8d8d8d_500x100.png')

@groundcontrol_app.route('/groundcontrol/images/ui-icons_ffffff_256x240.png')
def groundcontrol_jquery_image2():
    return groundcontrol_app.send_static_file('images/ui-icons_ffffff_256x240.png')

@groundcontrol_app.route('/groundcontrol/images/ui-bg_highlight-soft_75_5c635b_1x100.png')
def groundcontrol_jquery_image3():
    return groundcontrol_app.send_static_file('images/ui-bg_highlight-soft_75_5c635b_1x100.png')

@groundcontrol_app.route('/groundcontrol/images/ui-bg_glass_100_f6f6f6_1x400.png')
def groundcontrol_jquery_image4():
    return groundcontrol_app.send_static_file('images/ui-bg_glass_100_f6f6f6_1x400.png')

@groundcontrol_app.route('/groundcontrol/images/ui-icons_92908e_256x240.png')
def groundcontrol_jquery_image5():
    return groundcontrol_app.send_static_file('images/ui-icons_92908e_256x240.png')

@groundcontrol_app.route('/groundcontrol/images/ui-bg_glass_100_2f2f2e_1x400.png')
def groundcontrol_jquery_image6():
    return groundcontrol_app.send_static_file('images/ui-bg_glass_100_2f2f2e_1x400.png')
