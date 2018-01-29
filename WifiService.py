import os
import sqlite3
import random
import string


class WifiService:

    def __init__(self):
        path = 'database.db'
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)
            pass

    def get_wifi_connection(self):
        self.cur.execute('SELECT * FROM wifi_connections')
        row = self.cur.fetchone()
        return dict(zip(row.keys(), row))

    def __del__(self):
        self.conn.close()

def randomname(size = 64, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

service = WifiService()
json = service.get_wifi_connection()

try:
    (os.remove("application_logic/sensor_controller/test.txt"))
except OSError:
    print("file not there")
file_object = open("application_logic/sensor_controller/test.txt", 'w')

file_object.write('\n'.join([json["ssid"], json["password"], randomname()]) + '\n')
file_object.close()
