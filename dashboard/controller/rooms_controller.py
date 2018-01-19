import json

from flask import Blueprint, Response
from persistency.rooms_DAO import Rooms_DAO
from persistency.devices_DAO import Devices_DAO

api_rooms_blueprint = Blueprint('api-rooms', __name__, )

rooms_DAO = Rooms_DAO('C:\\Users\\Maarten\\Documents\\School\\2018\\Waterschade-dashboard\\database.db')
device_DAO = Devices_DAO('C:\\Users\\Maarten\\Documents\\School\\2018\\Waterschade-dashboard\\database.db')

@api_rooms_blueprint.route("/rooms")
def get_rooms():
    data = json.dumps(rooms_DAO.get_rooms())
    return Response(data, mimetype='application/json')

@api_rooms_blueprint.route('/rooms/<string:room_id>/sensors')
def get_room_sensors(room_id):
    data = json.dumps(device_DAO.get_devices_by_room_id(room_id))
    return Response(data, mimetype='application/json')