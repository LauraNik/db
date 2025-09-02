import sqlite3
from utils import get_connection

class ConnectSingleton:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection = get_connection()
            cls._connection.row_factory = sqlite3.Row
        return cls._instance

    @property
    def connection(self):
        return self._connection

    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            ConnectSingleton._instance = None
