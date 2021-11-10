from application import db
import os
from datetime import datetime
import json
import pytz
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
from sqlalchemy.dialects.postgresql import JSON as POSTGRES_JSON
dt_utcnow = datetime.now(tz=pytz.UTC)
local_time_now = dt_utcnow.astimezone(pytz.timezone('Europe/Helsinki'))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    name = db.Column(db.String(110), nullable=False)
    created_by = db.Column(db.String(110), nullable=False)
    
    if (os.getenv('HEROKU')):
        votes = db.Column(POSTGRES_JSON)
    else:
        votes = db.Column(SQLITE_JSON)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.votes = json.dumps({'users': []})

class WinnerTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    name = db.Column(db.String(110), nullable=False)
    created_by = db.Column(db.String(110), nullable=False)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
