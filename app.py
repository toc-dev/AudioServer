"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import secrets
import json
import os
import sqlite3
import datetime
from flask import Flask, request, jsonify, make_response, Response
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from models import Song, Podcast, Audiobook
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine("sqlite:///audio.db")
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

wsgi_app = app.wsgi_app
app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.db'
db = SQLAlchemy(app)

import requests
  

class UploadSong:
    def __init__(self, request):
        self.name = request.json['name']
        self.duration = request.json['duration']
    #uploaded_time = request.json['uploaded_time']

class UploadPodcast(UploadSong):
    def __init__(self, request):
        self.host = request.json['host']
        self.participants = request.json['participants']
        super().__init__(self)


class UploadAudiobook(UploadSong):
    def __init__(self, request):
        self.author = request.json['author']
        self.narrator = request.json['narrator']


@app.route('/create/<audioFileType>', methods=['POST'])
def create(audioFileType):

    if audioFileType == "song":
        upload_song = UploadSong(request)
        song = Song(name=upload_song.name, duration=upload_song.duration)
        db.session.add(song)
        
    if audioFileType == "podcast":
        upload_podcast = UploadPodcast(request)
        podcast = Podcast(name=upload_podcast.name, duration=upload_podcast.duration, host=upload_podcast.host, participants=upload_podcast.participants)
        db.session.add(podcast)

    if audioFileType == "audiobook":
        file = UploadAudiobook()
    db.session.commit()
@app.route('/delete/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete(audioFileType, audioFileID):
    if audioFileType == "song":
        song = db.session.query(Song).filter_by(id=audioFileID).one()
        db.session.delete(song)
        db.session.commit()
    if audioFileType == "podcast":
        podcast = db.session.query(Podcast).filter_by(id=audioFileID).one()
        db.session.delete(podcast)
        db.session.commit()
    if audioFileType == "audiobook":
        audiobook = db.session.query(Audiobook).filter_by(id=audioFileID).one()
        db.session.delete(audiobook)
        db.session.commit()
        
    return {"deleted": "deleted"}
    #if audioFileType == "song":
    #pass

@app.route('/update/<audioFileType>/<audioFileID>', methods=['PUT'])
def update(audioFileType, audioFileID):
    if audioFileType == "song":
        song = Song.query.get(audioFileID)
        song.name = name
        song.duration = duration

    pass

@app.route('/<audioFileType>/<audioFileID>', methods=['GET'])
def getAPI(audioFileType, audioFileID):
    if audioFileType == "song":
        song = Song.query.get(audioFileID)
        return jsonify({"name":song.name, "duration":song.duration, "uploaded_time":song.uploaded_time})
    pass


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
