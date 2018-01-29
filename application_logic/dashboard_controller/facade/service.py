import os
import sqlite3


class Service(object):
    """Service for the sensor package to interact with"""

    def __init__(self):
        path = './database.db'
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except:
            pass

    def add_new_device(self, device_id, name="water_sensor"):
        print(id, name)

    def report_water_damage(self, device_id):
        pass

    def check_if_sensor_present(self, device_id):
        self.cur.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
        exists = self.cur.fetchone()

        if exists is None:
            return False
        return True
