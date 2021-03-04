"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
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
from models import Song, Podcast, Audiobook,SongSchema,PodcastSchema,AudiobookSchema
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
song_schema = SongSchema()
songs_schema = SongSchema(many=True)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)
audiobook_schema = AudiobookSchema()
audiobooks_schema = AudiobookSchema(many=True)

class UploadSong:
    def __init__(self, request):
        self.name = request.json['name']
        self.duration = request.json['duration']
    #uploaded_time = request.json['uploaded_time']

class UploadPodcast(UploadSong):
    def __init__(self, request):
        self.host = request.json['host']
        self.participants = request.json['participants']
        super().__init__(request)


class UploadAudiobook(UploadSong):
    def __init__(self, request):
        self.author = request.json['author']
        self.narrator = request.json['narrator']
        super().__init__(request)

@app.route('/create/<audioFileType>', methods=['POST'])
def create(audioFileType):

    if audioFileType == "song":
        upload_song = UploadSong(request)
        song = Song(name=upload_song.name, duration=upload_song.duration)
        db.session.add(song)
        db.session.commit()
        return song_schema.jsonify(song)

    if audioFileType == "podcast":
        upload_podcast = UploadPodcast(request)
        podcast = Podcast(name=upload_podcast.name, duration=upload_podcast.duration, host=upload_podcast.host, participants=upload_podcast.participants)
        db.session.add(podcast)
        db.session.commit()
        return podcast_schema.jsonify(podcast)

    if audioFileType == "audiobook":
        upload_audiobook = UploadAudiobook(request)
        audiobook = Audiobook(name=upload_audiobook.name, duration=upload_audiobook.duration, 
                    author=upload_audiobook.author, narrator=upload_audiobook.narrator)
        db.session.add(audiobook)
        db.session.commit()
        return audiobook_schema.jsonify(audiobook)

    
    return {"success!": "success"}
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

@app.route('/update/<audioFileType>/<audioFileID>', methods=['PUT'])
def update(audioFileType, audioFileID):
    if audioFileType == "song":
        upload_song = UploadSong(request)
        song = Song.query.get(audioFileID)
        song.name = upload_song.name
        song.duration = upload_song.duration
        db.session.merge(song)
        db.session.commit()
        return song_schema.jsonify(song)

    if audioFileType == "podcast":
        upload_podcast = UploadPodcast(request)
        podcast = Podcast.query.get(audioFileID)
        podcast.name = upload_song.name
        podcast.duration = upload_song.duration
        podcast.host = upload_podcast.host
        podcast.participants = upload_podcast.participants
        db.session.merge(podcast)
        db.session.commit()
        return podcast_schema.jsonify(podcast)

    if audioFileType == "audiobook":
        upload_audiobook = UploadAudiobook(request)
        audiobook = Audiobook.query.get(audioFileID)
        audiobook.name = upload_audiobook.name
        audiobook.duration = upload_audiobook.duration
        audiobook.author = upload_audiobook.author
        audiobook.narrator = upload_audiobook.narrator
        db.session.merge(audiobook)
        db.session.commit()
        return audiobook_schema.jsonify(audiobook)
    
    

@app.route('/<audioFileType>/<audioFileID>', methods=['GET'])
def get_file(audioFileType, audioFileID):
    if audioFileType == "song":
        song = Song.query.get(audioFileID)
        return song_schema.jsonify(song)

    if audioFileType == "podcast":
        podcast = Podcast.query.get(audioFileID)
        return podcast_schema.jsonify(podcast)

    if audioFileType == "audiobook":
        audiobook = Audiobook.query.get(audioFileID)
        return audiobook_schema.jsonify(audiobook)
    
    
@app.route('/<audioFileType>/', methods=['GET'])
def get_all_files(audioFileType):
    if audioFileType == "song":
        song = Song.query.all()
        return songs_schema.jsonify(song)

    if audioFileType == "podcast":
        podcast = Podcast.query.all()
        return podcasts_schema.jsonify(podcast)

    if audioFileType == "audiobook":
        audiobook = Audiobook.query.all()
        return audiobooks_schema.jsonify(audiobook)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
