import sqlite3
from sqlite3 import Error
import os


class RoomsDAO(object):
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

    def get_rooms(self):
        try:
            self.cur.execute('SELECT * FROM rooms')
            rows = self.cur.fetchall()

            rooms_list = []

            for row in rows:
                rooms_list.append(dict(zip(row.keys(), row)))
            return rooms_list
        except Exception as e:
            # TODO implement logging - app.logger.Error(e)
            pass

    def get_room(self, room_id):
        self.cur.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        row = self.cur.fetchone()
        return dict(zip(row.keys(), row))

    def __del__(self):
        self.conn.close()
