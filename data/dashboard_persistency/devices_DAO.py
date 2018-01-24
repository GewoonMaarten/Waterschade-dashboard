import sqlite3
from sqlite3 import Error
import os


class DevicesDAO(object):
    """Database access object for the rooms table."""

    def __init__(self, path):
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except Error as e:
            # TODO implement logging - app.logger.Error(e)
            pass

    def get_devices_by_room_id(self, room_id):
        try:
            self.cur.execute('SELECT * FROM devices WHERE rooms_id = ?', room_id)
            rows = self.cur.fetchall()

            devices_list = []

            for row in rows:
                devices_list.append(dict(zip(row.keys(), row)))
            return devices_list
        except Exception as e:
            # TODO implement logging - app.logger.Error(e)
            pass

    def get_devices_from_room(self, room):
        self.cur.execute('SELECT * FROM devices WHERE rooms_id = ?', (room,))
        rows = self.cur.fetchall()

        devices_list = []

        for row in rows:
            devices_list.append(dict(zip(row.keys(), row)))
        return devices_list

    def update_device_status(self, device_id, status):
        print('Device=' + str(device_id) + ', status=' + str(status))
        self.cur.execute('UPDATE devices SET status = ? WHERE id = ?', (status, device_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
