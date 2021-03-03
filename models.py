import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import Model
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from flask_marshmallow import Marshmallow
app =  Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.db'
db = SQLAlchemy(app)

class Audio():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.Time, nullable=False)
    audio_file = db.Column(db.String(20), nullable=False)

class Song(db.Model, Audio):
    __tablename__ = 'songs'

class Podcast(db.Model, Audio):
    __tablename__ = 'podcasts'
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(20))

class Audiobook(db.Model, Audio):
    __tablename__ = 'audiobook'
    author = db.Column(db.String(100), unique=True, nullable=False)
    narrator = db.Column(db.String(100), unique=True, nullable=False)

    #db.MutableList.as_mutable(PickleType), default=[])