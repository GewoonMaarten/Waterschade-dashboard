import json

from flask import render_template, abort, Response, request
from data.dashboard_persistency.facade.service import Service as Persistency_service

from application_logic.dashboard_controller import app

persistency_service = Persistency_service('./database.db')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/users')
def get_users():
    return ''


@app.route('/api/temperature/<string:city>')
def temperature(city):
    # TODO retrieve automatically temperature from argued city
    data = 13
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/api/devices/active')
def active_devices():
    # TODO retrieve all active devices
    data = 3
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/api/damages')
def water_damages():
    # TODO retrieve all active devices
    damages = [0, 1, 2, 6, 8]
    return Response(json.dumps(damages), mimetype='application/json')


@app.route('/api/rooms/<int:room_id>/devices/<int:device_id>', methods=['PUT'])
def update_sensor_name(room_id, device_id):
    form = request.form
    print(form['active'] == 'true')
    if 'name' in form:
        print('name found=' + form['name'])
    elif 'active' in form:
        persistency_service.update_device_status(device_id, 1 if form['active'] == 'true' else 0)
    error = None
    response = {
        'error': error
    }
    return Response(json.dumps(response), mimetype='application/json')


@app.route('/api/devices/get')
def get_unnamed_devices():
    # get all unnamed devices from the database so user can fill name for them

    # dummy data
    devices = [
        {
            'id': 1
        }
    ]
    return Response(json.dumps(devices), mimetype='application/json')


@app.route('/api/rooms')
def get_rooms():
    data = persistency_service.get_rooms_as_json()
    return Response(data, mimetype='application/json')


@app.route('/api/rooms/<string:room>/devices')
def get_room_devices(room):
    data = persistency_service.get_devices_from_room(room)
    return Response(data, mimetype='application/json')
