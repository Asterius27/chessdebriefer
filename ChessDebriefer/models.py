from mongoengine import *


# missing fields: time
# required fields?
class Games(Document):
    event = StringField()
    site = URLField()
    white = StringField()
    black = StringField()
    result = StringField()
    date = DateField()
    white_elo = IntField()
    black_elo = IntField()
    white_rating_diff = IntField()
    black_rating_diff = IntField()
    eco = StringField()
    opening = StringField()
    time_control = StringField()
    termination = StringField()
    moves = StringField()  # best way?


# document used as cache
class Players(Document):
    name = StringField()
    percentages = DictField()


# document used as cache
class FieldsCache(Document):
    event = ListField(StringField())
    opening = ListField(StringField())
    termination = ListField(StringField())
