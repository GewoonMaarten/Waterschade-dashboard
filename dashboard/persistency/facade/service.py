from ConfigParser import ConfigParser
from util.config_parser import config_section_map

from persistency.user_DAO import User_DAO
from persistency.rooms_DAO import Rooms_DAO
class Service(object):
    def __init__(self, path):
        # ConfigParser.config_section_map = config_section_map

        # Config = ConfigParser()
        # Config.read(config_path)

        # self.db_path = Config.config_section_map('database')['path']
        self.user_DAO = User_DAO(self.path)
        self.rooms_DAO = Rooms_DAO(self.path)

    def save_user(self, email, password):
        self.user_DAO.create_user(email, password)


    def get_rooms_as_json():
        return json.dumps(self.rooms_DAO.get_rooms())
    def get_devices_by_room_id_as_json(room_id):
        return json.dumps(self.rooms_DAO.get_devices_by_room_id(room_id))