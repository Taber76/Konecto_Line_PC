from peewee import Model, CharField, BooleanField, UUIDField
from db.conection import DbConnection


class UserRole:
    ADMIN = 'ADMIN'
    MAINT = 'MAINT'
    OPER = 'OPER'
    VIEWER = 'VIEWER'

    CHOICES = [
        (ADMIN, 'Admin'),
        (MAINT, 'Maintenance'),
        (OPER, 'Operator'),
        (VIEWER, 'Viewer')
    ]


class User(Model):
    id = UUIDField(primary_key=True)
    fullname = CharField(max_length=255)
    username = CharField(unique=True, max_length=255)
    password = CharField(max_length=255)
    role = CharField(choices=UserRole.CHOICES)
    active = BooleanField()

    class Meta:
        database = DbConnection().db
        table_name = 'users'
