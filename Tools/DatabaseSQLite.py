import os
import sqlite3


class DB:
    def __init__(self, name: str = 'currency.db'):
        self.dbname: str = name
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        if self.check_and_create_database():
            print('Base de datos creada con exito')
        else:
            print('Ya existe la base de datos.')

    def create_database(self):
        create_table_query: str = '''
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            date TEXT NOT NULL
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def check_and_create_database(self) -> bool:
        if not os.path.exists(self.dbname):
            self.open_connection()
            self.create_database()
            return True

        return False

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def open_connection(self):
        self.connection = sqlite3.connect(self.dbname)
        self.cursor = self.connection.cursor()

    def insert_data(self, var, name: str, date):
        print('Insertando...')
        self.open_connection()

        query = f'''
            INSERT INTO rates (name, value, date) VALUES (?, ?, ?)
        '''

        self.cursor.execute(query, (name, var, date))
        self.connection.commit()

        print('Finalizado...')

