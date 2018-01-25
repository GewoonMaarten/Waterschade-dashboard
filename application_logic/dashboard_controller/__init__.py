from flask import Flask

app = Flask(__name__, template_folder='../../templates', static_folder='../../static')

from application_logic.dashboard_controller import routes
