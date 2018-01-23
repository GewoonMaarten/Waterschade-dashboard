import json

from flask import Blueprint

api_devices_blueprint = Blueprint('api-devices', __name__, )

@api_devices_blueprint.route('/sensors/get', methods = ['GET'])
def get_unnamed_sensors():
    # get all unnamed sensors from the database

    # dummy data
    sensors = [
        {
            'id': 1
        }
    ]
    return json.dumps(sensors)