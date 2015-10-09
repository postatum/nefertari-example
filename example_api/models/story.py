from nefertari import engine as eng
from nefertari.engine import BaseDocument


class Story(BaseDocument):
    _auth_fields = [
        'id', 'start_date', 'due_date', 'name', 'description', 'progress']
    _public_fields = ['id', 'start_date', 'due_date', 'name']

    id = eng.IdField(primary_key=True)
    updated_at = eng.DateTimeField()
    name = eng.StringField(required=True)
    description = eng.TextField(required=True)
    progress = eng.FloatField()
    completed = eng.BooleanField()
    signs_number = eng.BigIntegerField()
    valid_date = eng.DateField()
    valid_time = eng.TimeField()
    reads = eng.IntegerField()
    rating = eng.SmallIntegerField()
