import logging

import cryptacular.bcrypt

from nefertari import engine as eng
from nefertari.engine import BaseDocument

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
log = logging.getLogger(__name__)


class Profile(BaseDocument):
    id = eng.IdField(primary_key=True)
    updated_at = eng.DateTimeField()
    created_at = eng.DateTimeField()
    address = eng.UnicodeTextField()


class User(BaseDocument):
    _nested_relationships = ['profile', 'stories']
    _auth_fields = ['username', 'first_name', 'last_name', 'stories']
    _public_fields = ['username']
    _hidden_fields = ['password']

    username = eng.StringField(primary_key=True)
    email = eng.StringField(required=True)
    password = eng.StringField(required=True)
    updated_at = eng.DateTimeField()
    first_name = eng.StringField()
    last_name = eng.StringField()
    last_login = eng.DateTimeField()
    stories = eng.Relationship('Story', backref_name='owner')
    profile = eng.Relationship('Profile', uselist=False)
