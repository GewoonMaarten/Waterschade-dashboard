import json

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sensors/get')
def get_unnamed_sensors():
    # get all unnamed sensors from the database

    # dummy data
    sensors = [
        {
            'id': 1
        }
    ]
    return json.dumps(sensors)


@app.route('/rooms')
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


@app.route('/rooms/<string:room_id>/sensors')
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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
