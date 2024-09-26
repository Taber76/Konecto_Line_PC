from peewee import DoesNotExist

from db.conection import DbConnection
from db.sessions.model import Session


def session_register(line_id, batch_id, start_time):
    try:
        with DbConnection('cloud').db.connection_context():
            return Session.create(
                line_id=line_id,
                batch_id=batch_id,
                start_time=start_time,
                end_time=start_time,
                quantity=0,
                defects=0
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def session_update(id, end_time=None, quantity=None, defects=None, downtime_minutes=None):
    try:
        with DbConnection('cloud').db.connection_context():
            session = Session.get(Session.id == id)

            if end_time is not None:
                session.end_time = end_time
            if quantity is not None:
                session.quantity = quantity
            if defects is not None:
                session.defects = defects
            if downtime_minutes is not None:
                session.downtime_minutes = downtime_minutes

            session.save()
            return session
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
