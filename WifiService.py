import os
import sqlite3


class WifiService:

    def __init__(self):
        path = '../../database.db'
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
