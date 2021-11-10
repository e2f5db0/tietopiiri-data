from application import db
from datetime import datetime
import pytz
dt_utcnow = datetime.now(tz=pytz.UTC)
local_time_now = dt_utcnow.astimezone(pytz.timezone('Europe/Helsinki'))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    name = db.Column(db.String(110), nullable=False)
    created_by = db.Column(db.String(110), nullable=False)
    votes = db.Column(db.Integer)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.votes = 0

class WinnerTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    name = db.Column(db.String(110), nullable=False)
    created_by = db.Column(db.String(110), nullable=False)
    votes = db.Column(db.Integer)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.votes = 0

