import sqlite3
import os

class Users_DAO(object):
    'Database access object for the user table.'

    def __init__(self, path):

        try:
            if os.path.exists(path):
                self.conn = sqlite3.connect(path, check_same_thread=False)
                self.cur = self.conn.cursor()
        except Error as e:
           print(e)

    def create_user(self, email, password):

        try:
            self.cur.execute('INSERT INTO users(email, password) VALUES(?,?)', (email, password,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.cur.close()

    def get_user_by_email(self, email):
        self.c.execute('SELECT id, email, password FROM users WHERE email=?', (email,))
        return self.c.fetchone()

    def update_user(self, email, password):
        self.c.execute('UPDATE users SET password=? where email=?', (email, password,))
        self.conn.commit()

    def delete_user(self, email):
        self.c.execute('DELETE FROM users WHERE email=?', (email,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()