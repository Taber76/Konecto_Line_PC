from peewee import Model, CharField, IntegerField, DateTimeField, UUIDField
from db.conection import DbConnection


class CountInterval:
    SECONDS = 'SECONDS'
    MINUTES = 'MINUTES'
    DAYS = 'DAYS'
    WEEKS = 'WEEKS'
    MONTHS = 'MONTHS'
    YEARS = 'YEARS'

    CHOICES = [
        (SECONDS, 'Seconds'),
        (MINUTES, 'Minutes'),
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
        (MONTHS, 'Months'),
        (YEARS, 'Years')
    ]


class Count(Model):
    id = UUIDField(primary_key=True)
    session_id = CharField(max_length=255)
    time_stamp = DateTimeField()
    quantity = IntegerField()
    defects = IntegerField()
    time_diff = IntegerField()
    interval = CharField(choices=CountInterval.CHOICES)

    class Meta:
        database = DbConnection().db
        table_name = 'counts'
