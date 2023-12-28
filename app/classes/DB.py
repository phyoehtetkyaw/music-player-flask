import sqlite3

class DB:
    @staticmethod
    def connect_db():
        conn = None

        try:
            conn = sqlite3.connect("db_music.sqlite")
        except sqlite3.error as e:
            print(e)

        return conn