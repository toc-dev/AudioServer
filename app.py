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
  

#class UploadSong():
#    name = request.json['name_of_audio']
#    duration = request.json['duration']
#    uploaded_time = request.json['uploaded_time']

#class UploadPodcast(UploadSong):
#    host = request.json['host']
#    participants = request.json['participants']


#class UploadAudiobook(UploadSong):
#    author = request.json['author']
#    narrator = request.json['narrator']


@app.route('/create/<audioFileType>', methods=['POST'])
def create(audioFileType):

    if audioFileType == "song":
        upload_song = UploadSong()
        name = request.json['name']
        duration = request.json['duration']
        uploaded_time = datetime.datetime.now()

        song = Song(name=upload_song.name, duration=upload_song.duration)
        session.add(song)
        session.commit()

    if audioFileType == "podcast":
        file = UploadPodcast()
    if audioFileType == "audiobook":
        file = UploadAudiobook()

@app.route('/delete/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete(audioFileType, audioFileID):
    if audioFileType == "song":
        song = Song.query.get(audioFileID).delete()
        #song.delete()
        db.session.delete(song)
        session.commit()
        #db.session.delete(the_song)
        
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
