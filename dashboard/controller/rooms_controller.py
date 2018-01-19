import json

from flask import Blueprint

api_rooms_blueprint = Blueprint('api-rooms', __name__, )

@api_rooms_blueprint.route("/rooms")
def get_rooms():
    rooms = [
        {
            'id': 3,
            'name': 'Hallo jumbo'
        },
        {
            'id': 5,
            'name': 'Hoogvliet altijd nummer 1'
        }
    ]
    return json.dumps(rooms)

@api_rooms_blueprint.route('/rooms/<string:room_id>/sensors')
def get_room_sensors(room_id):
    # TODO Get sensors for argued room id

    # dummy data
    sensors = [
        {
            'id': 'Hallo',
            'name': 'Idk sensor',
            'status': 0
        },
        {
            'id': 'FF29DF',
            'name': 'Tweede sensor',
            'status': 1
        }
    ]
    return json.dumps(sensors)