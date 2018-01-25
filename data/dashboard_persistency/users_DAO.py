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

    def __del__(self):
        self.conn.close()
