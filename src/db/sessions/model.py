from peewee import Model, CharField, IntegerField, DateTimeField, UUIDField
from db.conection import DbConnection


class Session(Model):
    id = UUIDField(primary_key=True)
    line_id = CharField(max_length=255)
    batch_id = CharField(max_length=255)
    start_time = DateTimeField()
    end_time = DateTimeField()
    quantity = IntegerField()
    defects = IntegerField()
    downtime_minutes = IntegerField()

    class Meta:
        database = DbConnection().db
        table_name = 'sessions'
