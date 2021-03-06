import sqlite3
from sqlite3 import Error
import os
import datetime
import time


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

    def get_devices_from_room(self, room):
        try:
            self.cur.execute('SELECT * FROM devices WHERE rooms_id = ?', (room,))
            rows = self.cur.fetchall()

            devices_list = []

            for row in rows:
                devices_list.append(dict(zip(row.keys(), row)))
            return devices_list
        except Exception as e:
            # TODO implement logging - app.logger.Error(e)
            pass

    def get_device_name(self, device_id):
        self.cur.execute('SELECT name FROM devices WHERE id = ?', (device_id,))
        row = self.cur.fetchone()
        test = dict(zip(row.keys(), row))
        return test

    def update_device_name(self, device_id, name):
        self.cur.execute('UPDATE devices SET name = ? WHERE id = ?', (name, device_id))
        self.conn.commit()
        return True

    def update_device_status(self, device_id, status):
        self.cur.execute('UPDATE devices SET status = ? WHERE id = ?', (status, device_id))
        self.conn.commit()
        return True

    def update_device_room(self, device_id, rooms_id):
        self.cur.execute('UPDATE devices SET rooms_id = ?, status=1 WHERE id = ?', (rooms_id, device_id))
        self.conn.commit()
        return True    

    def get_device(self, device_id):
        self.cur.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
        return self.cur.fetchone()

    def add_device(self, device_id, device_name):
        self.cur.execute('INSERT INTO devices(id,status,name) VALUES (?,1,?)', (device_id,device_name))
        self.conn.commit()
        return True
        
    def get_active_devices(self):
        self.cur.execute('SELECT * FROM devices WHERE status = ?', (1,))
        devices_list = []

        rows = self.cur.fetchall()

        for row in rows:
            devices_list.append(dict(zip(row.keys(), row)))
        return devices_list

    def get_all_devices_without_room(self):
        try:
            self.cur.execute('SELECT * FROM devices WHERE rooms_id IS NULL')

            devices_list = []

            rows = self.cur.fetchall()

            for row in rows:
                devices_list.append(dict(zip(row.keys(), row)))
            return devices_list
        except Error as e:
            pass

    def report_water_damage(self, device_id):
        date = datetime.datetime.now()
        self.cur.execute('INSERT INTO water_damages(date, devices_id) VALUES(?,?)', (date, device_id))
        self.conn.commit()


    def add_wifi_connection(self, ssid, password):
        self.cur.execute('INSERT INTO wifi_connections (`ssid`, `password`) VALUES (' + ssid + ', ' + password + ')')
        self.conn.commit()
        return True

    def __del__(self):
        self.conn.close()
