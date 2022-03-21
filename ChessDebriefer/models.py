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
    opening_id = ObjectIdField()
    time_control = StringField()
    termination = StringField()
    moves = StringField()
    best_moves = ListField(StringField())
    moves_evaluation = ListField(StringField())


# document used as cache
class FieldsCache(Document):
    event = ListField(StringField())
    opening_id = ListField(ObjectIdField())
    eco = ListField(StringField())
    termination = ListField(StringField())


# document used as cache
class Players(Document):
    name = StringField(unique=True)
    elo = IntField()
    elo_date = DateField()
    openings = DictField()
    terminations = DictField()
    events = DictField()
    accuracy = DictField()
    percentages = DictField()


class Openings(Document):
    eco = StringField()
    white_opening = StringField()
    black_opening = StringField()
    moves = StringField()
    engine_evaluation = StringField()
