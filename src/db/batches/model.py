from peewee import Model, CharField, IntegerField, DateTimeField, UUIDField
from db.conection import DbConnection


class Batch(Model):
    id = UUIDField(primary_key=True)
    code = CharField(max_length=255)
    product_id = CharField(max_length=255)
    product_name = CharField(max_length=255)
    total_produced = IntegerField()
    total_defects = IntegerField()
    downtime_minutes = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        database = DbConnection().db
        table_name = 'batchs_detail'  # 'batches_detail' is a view
        primary_key = False
