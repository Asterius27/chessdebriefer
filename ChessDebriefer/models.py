from mongoengine import *


class Games(Document):
    name = StringField()
