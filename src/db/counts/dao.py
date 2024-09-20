from peewee import DoesNotExist

from db.conection import DbConnection
from db.counts.model import Count


def count_register(timestamp, session_id, quantity, defects, time_diff, interval):
    try:
        with DbConnection().db.connection_context():
            return Count.create(
                timestamp=timestamp,
                session_id=session_id,
                quantity=quantity,
                defects=defects,
                time_diff=time_diff,
                interval=interval
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
