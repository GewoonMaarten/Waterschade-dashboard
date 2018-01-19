import sqlite3
from sqlite3 import Error
import itertools
import os

class Rooms_DAO(object):
    'Database access object for the rooms table.'

    def __init__(self, path):
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except Error as e:
           print(e)


    def get_rooms(self):
        try:
            self.cur.execute('SELECT * FROM rooms')
            rows = self.cur.fetchall()

            rooms_list = []

            for row in rows:
                rooms_list.append(dict(itertools.izip(row.keys(), row)))
            return rooms_list
        except Exception as e:
            print('Error: ', e)

    def __del__(self):
        self.conn.close()