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

    # TODO staticmethod
    @property
    def connection(self):
        return self._connection
    # TODO remove
    def cursor(self):
        return self._connection.cursor()
    # TODO remove
    def commit(self):
        self._connection.commit()
    # TODO remove
    def rollback(self):
        self._connection.rollback()
    # TODO staticmethod
    def close(self):
        if self._connection:
            self._connection.close()
            # TODO
            self._connection = None
            ConnectSingleton._instance = None
