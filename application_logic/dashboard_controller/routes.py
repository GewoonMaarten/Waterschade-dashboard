import json
import flask
import flask_login

from flask import render_template, Response, request

from application_logic.dashboard_controller.authentication.User import User
from data.dashboard_persistency.facade.service import Service as Persistency_service

from application_logic.dashboard_controller import app

PERSISTENCY_SERVICE = Persistency_service('./database.db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email']
    user = PERSISTENCY_SERVICE.get_user_by_email(email)

    if user is None:
        return Response(json.dumps({
            'error': 'RIP'
        }), mimetype='application/json')

    if flask.request.form['password'] == user['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return Response(json.dumps({
            'success': True
        }))

    return 'Bad login'


@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('login'))


@app.route('/')
@flask_login.login_required
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
    response = {}
    if 'name' in form:
        PERSISTENCY_SERVICE.update_device_name(device_id, form['name'])
        response['name'] = form['name']
    elif 'active' in form:
        PERSISTENCY_SERVICE.update_device_status(device_id, 1 if form['active'] == 'true' else 0)
        response['active'] = True if form['active'] == 'true' else False
    response['error'] = None
    print(response)
    return Response(json.dumps(response), mimetype='application/json')


@app.route('/api/rooms/<int:room_id>/devices/<int:device_id>/name', methods=['GET'])
def get_device_name(room_id, device_id):
    name = PERSISTENCY_SERVICE.get_device_name(device_id)
    return Response(json.dumps(name), mimetype='application/json')


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


@app.route('/api/devices/new')
def get_new_devices():
    devices = PERSISTENCY_SERVICE.get_all_devices_without_room()
    return Response(json.dumps(devices), mimetype='application/json')


@app.route('/api/rooms')
def get_rooms():
    data = PERSISTENCY_SERVICE.get_rooms_as_json()
    return Response(data, mimetype='application/json')


@app.route('/api/rooms/<string:room>/devices')
def get_room_devices(room):
    data = PERSISTENCY_SERVICE.get_devices_from_room(room)
    return Response(data, mimetype='application/json')
