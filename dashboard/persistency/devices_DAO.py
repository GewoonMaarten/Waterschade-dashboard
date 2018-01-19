import sqlite3
from sqlite3 import Error
import itertools
import os

class Devices_DAO(object):
    'Database access object for the rooms table.'

    def __init__(self, path):
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except Error as e:
           print(e)


    def get_devices_by_room_id(self, room_id):
        try:
            self.cur.execute('SELECT * FROM devices WHERE rooms_id = ?', room_id)
            rows = self.cur.fetchall()

            devices_list = []

            for row in rows:
                devices_list.append(dict(itertools.izip(row.keys(), row)))
            return devices_list
        except Exception as e:
            print('Error: ', e)

    def __del__(self):
        self.conn.close()
