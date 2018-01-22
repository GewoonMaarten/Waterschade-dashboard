import json
from flask import Flask, render_template, abort, Blueprint
from jinja2 import TemplateNotFound
import logging
from logging.handlers import RotatingFileHandler
from config import DevelopmentConfig

from controller.rooms_controller import api_rooms_blueprint
from controller.devices_controller import api_devices_blueprint

app = Flask(__name__)

app.register_blueprint(api_rooms_blueprint, url_prefix="/api")
app.register_blueprint(api_devices_blueprint, url_prefix="/api")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.debug = True

    app.run(host='0.0.0.0')
