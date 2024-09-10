from peewee import PostgresqlDatabase, Model, CharField
from threading import Lock

from config.environment import DATABASE_URL


class DbConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.db = PostgresqlDatabase(None)
                cls._instance.db.init(DATABASE_URL)
            return cls._instance

    def connect(self):
        if not self.db.is_connection_usable():
            self.db.connect()

    def close(self):
        if not self.db.is_closed():
            self.db.close()
