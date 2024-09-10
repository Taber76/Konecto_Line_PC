from peewee import DoesNotExist

from db.conection import DbConnection
from db.batches.model import Batch


def get_all():
    try:
        with DbConnection().db.connection_context():
            return list(Batch.select())
    except DoesNotExist:
        print(f"Batch does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
