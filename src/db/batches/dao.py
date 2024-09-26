from peewee import DoesNotExist

from db.conection import DbConnection
from db.batches.model import Batch, Batch_Detail


def get_all_batches():
    try:
        with DbConnection('cloud').db.connection_context():
            return list(Batch_Detail.select())
    except DoesNotExist:
        print(f"Batch does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def batch_update(id, quantity, defects, downtime_minutes, updated_at):
    try:
        with DbConnection('cloud').db.connection_context():
            batch = Batch.get(Batch.id == id)
            batch.total_produced = batch.total_produced + quantity
            batch.total_defects = batch.total_defects + defects
            batch.downtime_minutes = batch.downtime_minutes + downtime_minutes
            batch.updated_at = updated_at
            batch.save()
            return batch
    except Exception as e:
        print("------------------------------------------------------------")
        print(f"An error occurred: {e}")
        return None
