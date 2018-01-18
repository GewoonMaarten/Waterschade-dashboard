import sqlite3


class User_DAO:

    conn = sqlite3.connect('../../database.db')

    def __init__(self):
        self.c = conn.cursor()

    def create_user(email, password):
        self.c.execute('INSERT INTO user(email, password) VALUES(?,?)', email, password)
        conn.commit()

    def __del__(self):
        conn.close()
