import json

from flask import render_template, abort, Response, request
from jinja2 import TemplateNotFound

from application_logic.dashboard_controller import app

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


@app.route('/api/sensors/active')
def active_sensors():
    # TODO retrieve all active sensors
    data = 3
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/api/damages')
def water_damages():
    # TODO retrieve all active sensors
    damages = [0, 1, 2, 6, 8]
    return Response(json.dumps(damages), mimetype='application/json')


@app.route('/api/rooms/<int:room_id>/<string:sensor_id>', methods=['PUT'])
def update_sensor_name(room_id, sensor_id):
    form = request.form
    if 'name' in form:
        print('name found=' + form['name'])
    elif 'active' in form:
        print('active found=' + form['active'])

    print(str(room_id) + ' -> ' + sensor_id)
    # room = [room for room in rooms if room['id'] == room_id]
    error = None
    response = {
        'error': error
    }
    return Response(json.dumps(response), mimetype='application/json')


@app.route('/api/sensors/get')
def get_unnamed_sensors():
    # get all unnamed sensors from the database so user can fill name for them

    # dummy data
    sensors = [
        {
            'id': 1
        }
    ]
    return Response(json.dumps(sensors), mimetype='application/json')


@app.route('/api/rooms')
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
    return Response(json.dumps(rooms), mimetype='application/json')


@app.route('/api/rooms/<string:room_id>/sensors')
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
    return Response(json.dumps(sensors), mimetype='application/json')
