import json
from flask import Blueprint, Response
from data.dashboard_persistency.facade.service import Service as Persistency_service

api_rooms_blueprint = Blueprint('api-rooms', __name__)

persistency_service = Persistency_service('C:\\Users\\Maarten\\Documents\\School\\2018\\Waterschade-dashboard\\database.db')

@api_rooms_blueprint.route('/rooms', methods = ['GET'])
def get_rooms():
    data = persistency_service.get_rooms_as_json()
    return Response(data, mimetype='application/json')

@api_rooms_blueprint.route('/rooms/<string:room_id>/sensors', methods = ['GET'])
def get_room_sensors(room_id):
    data = persistency_service.get_devices_by_room_id_as_json(room_id)
    return Response(data, mimetype='application/json')