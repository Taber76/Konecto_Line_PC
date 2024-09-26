from peewee import Model, CharField, DateTimeField, UUIDField
from db.conection import DbConnection


class Log(Model):
    id = UUIDField(primary_key=True)
    session_id = CharField(max_length=255)
    user_id = CharField(max_length=255)
    username = CharField(max_length=255)
    timestamp = DateTimeField()
    description = CharField(max_length=255)

    class Meta:
        database = DbConnection('cloud').db
        table_name = 'logs'
