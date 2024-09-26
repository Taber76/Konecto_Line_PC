from peewee import PostgresqlDatabase
from threading import Lock

from config.environment import CLOUD_DATABASE
from config.environment import LOCAL_DATABASE


class DbConnection:
    _instances = {}
    _lock = Lock()

    def __new__(cls, db_name):
        with cls._lock:
            if db_name not in cls._instances:
                instance = super().__new__(cls)
                instance.db = PostgresqlDatabase(db_name)
                if db_name == 'cloud':
                    instance.db.init(CLOUD_DATABASE)
                else:
                    instance.db.init(LOCAL_DATABASE)
                cls._instances[db_name] = instance
            return cls._instances[db_name]

    def connect(self):
        if not self.db.is_connection_usable():
            self.db.connect()

    def close(self):
        if not self.db.is_closed():
            self.db.close()

    def is_connected(self):
        return self.db.is_connection_usable()