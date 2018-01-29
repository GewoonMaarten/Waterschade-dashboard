import sqlite3
from sqlite3 import Error
import os


class UsersDAO(object):
    """Database access object for the user table."""

    def __init__(self, path):
        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self.cur = self.conn.cursor()
        except Error as e:
            # TODO implement logging - app.logger.Error(e)
            pass

    def create_user(self, email, password):
        try:
            self.cur.execute('INSERT INTO users(email, password) VALUES(?,?)', (email, password,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.cur.close()

    def get_user_by_email(self, email):
        self.cur.execute('SELECT id, email, password FROM users WHERE email=?', (email,))
        return self.cur.fetchone()

    def update_user(self, email, password):
        self.cur.execute('UPDATE users SET password=? where email=?', (email, password,))
        self.conn.commit()

    def delete_user(self, email):
        self.cur.execute('DELETE FROM users WHERE email=?', (email,))
        self.conn.commit()

    def get_wifi_connections(self):
        self.cur.execute('SELECT * FROM wifi_connections')
        row = self.cur.fetchone()
        if row is None:
            return None
        return dict(zip(row.keys(), row))

    def add_wifi_connection(self, ssid, password):
        l = self.get_wifi_connections()
        if l is None:
            self.cur.execute(
                'INSERT INTO wifi_connections (id, ssid, password) VALUES (?, ?, ?)', (1, ssid, password)
            )
        else:
            self.cur.execute('UPDATE wifi_connections SET ssid = ?, password = ? WHERE id = 1', (ssid, password))
        self.conn.commit()
        return True

    def __del__(self):
        self.conn.close()
