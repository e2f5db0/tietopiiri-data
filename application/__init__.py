# flask-app
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

from dotenv import load_dotenv
load_dotenv()

# database
import os
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///topics.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# functionality
from application import views

from application.topics import models
from application.topics import views

#try:
db.create_all()
#except:
    #pass


