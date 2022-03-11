from mongoengine import *


# missing fields: time
# required fields, other constraints?
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
    best_moves = ListField(StringField())
    moves_evaluation = ListField(StringField())


# document used as cache, needed?
class Players(Document):
    name = StringField()
    percentages = DictField()


# document used as cache
class FieldsCache(Document):
    event = ListField(StringField())
    opening = ListField(StringField())
    termination = ListField(StringField())


class Openings(Document):
    eco = StringField()
    white_opening = StringField()
    black_opening = StringField()
    moves = StringField()
