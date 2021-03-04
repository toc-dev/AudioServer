import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import Model
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from flask_marshmallow import Marshmallow
import datetime
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
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class Song(db.Model, Audio):
    __tablename__ = 'songs'

class SongSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "duration", "uploaded_time")

class Podcast(db.Model, Audio):
    __tablename__ = 'podcasts'
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(20))

class PodcastSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "duration", "uploaded_time", "host", "participants")

class Audiobook(db.Model, Audio):
    __tablename__ = 'audiobook'
    author = db.Column(db.String(100), unique=True, nullable=False)
    narrator = db.Column(db.String(100), unique=True, nullable=False)

class AudiobookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "duration", "uploaded_time", "author", "narrator")
    #db.MutableList.as_mutable(PickleType), default=[])