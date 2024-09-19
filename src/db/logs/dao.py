from peewee import DoesNotExist

from db.conection import DbConnection
from db.logs.model import Log


def log_register(session_id, user_id, username, timestamp, description):
    try:
        with DbConnection().db.connection_context():
            return Log.create(
                session_id=session_id,
                user_id=user_id,
                username=username,
                timestamp=timestamp,
                description=description
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
