from flask import render_template, abort
from jinja2 import TemplateNotFound

from application_logic.dashboard_controller.devices_controller import api_devices_blueprint
from application_logic.dashboard_controller.rooms_controller import api_rooms_blueprint
from application_logic.dashboard_controller import app

app.register_blueprint(api_rooms_blueprint, url_prefix="/api")
app.register_blueprint(api_devices_blueprint, url_prefix="/api")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)