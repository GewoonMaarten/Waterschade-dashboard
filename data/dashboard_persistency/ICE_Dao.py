import sqlite3
from sqlite3 import Error
import os


class ICEDao(object):
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

    def create_contact(self, name, email, phone_number):
        try:
            self.cur.execute('INSERT INTO ice(name, email, phone_number) VALUES(?, ?, ?)', (name, email, phone_number,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.cur.close()

    def get(self, contact_id):
        self.cur.execute('SELECT * FROM ice WHERE id = ?', (contact_id,))
        row = self.cur.fetchone()
        return dict(zip(row.keys(), row))

    def get_all(self):
        self.cur.execute('SELECT * FROM ice')
        rows = self.cur.fetchall()

        contacts = []

        for row in rows:
            contacts.append(dict(zip(row.keys(), row)))
        return contacts

    def delete_contact(self, contact_id):
        self.cur.execute('DELETE FROM ice WHERE id=?', (contact_id,))
        return True

    def __del__(self):
        self.conn.close()
