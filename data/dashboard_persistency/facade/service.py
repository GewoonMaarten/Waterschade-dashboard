import json

from data.dashboard_persistency.users_DAO import UsersDAO
from data.dashboard_persistency.rooms_DAO import RoomsDAO
from data.dashboard_persistency.devices_DAO import DevicesDAO


class Service(object):
    def __init__(self, path):
        # ConfigParser.config_section_map = config_section_map

        # Config = ConfigParser()
        # Config.read(config_path)

        # self.db_path = Config.config_section_map('database')['path']
        self.user_DAO = UsersDAO(path)
        self.rooms_DAO = RoomsDAO(path)
        self.devices_DAO = DevicesDAO(path)

    def save_user(self, email, password):
        self.user_DAO.create_user(email, password)

    def get_user_by_email(self, email):
        return self.user_DAO.get_user_by_email(email=email)

    def get_rooms_as_json(self):
        return json.dumps(self.rooms_DAO.get_rooms())

    def get_devices_by_room_id_as_json(self, room_id):
        return json.dumps(self.rooms_DAO.get_devices_by_room_id(room_id))

    def get_devices_from_room(self, room):
        return json.dumps(self.devices_DAO.get_devices_from_room(room))

    def get_device_name(self, device_id):
        return json.dumps(self.devices_DAO.get_device_name(device_id))

    def update_device_name(self, device_id, name):
        return json.dumps(self.devices_DAO.update_device_name(device_id, name))

    def update_device_status(self, device_id, status):
        return json.dumps(self.devices_DAO.update_device_status(device_id, status))

    def get_device(self, device_id):
        return self.devices_DAO.get_device(device_id)

    def add_device(self, device_id):
        return self.add_device(device_id)