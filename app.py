"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import secrets
import json
import os
import sqlite3
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

class AudioForm(FlaskForm):
    audio = FileField(validators=[FileAllowed(['mp3', 'aa', 'aax', 'aac'])])
    #submit =  SubmitField('Submit')
    #myFile = secure_filename(form.fileName.file.filename)
    #form.fileName.file.save(PATH+myFile)
  

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


def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.root_path, 'static/audiofiles', audio_fn)
    form_audio.save(audio_path)

    return audio_fn

@app.route('/create/<audioFileType>', methods=['POST'])
def create(audioFileType):
    form = AudioForm()
    #body = request.get_json(force=True)
    #if form.validate_on_submit():
    #    if form.audio.data:
    #audio_file = save_audio(form.audio.data)
    if audioFileType == "song":
        #file = UploadSong()
        audio_file = request.form.get('audio_file')
        #if not audio_file:
        #    return 'no pic uploaded', 400
        name = request.json['name']
        duration = request.json['duration']
        uploaded_time = request.json['uploaded_time']
        song = Song(name=name, duration=duration, uploaded_time=uploaded_time)
        session.add(song)
        session.commit()
    if audioFileType == "podcast":
        file = UploadPodcast()
    if audioFileType == "audiobook":
        file = UploadAudiobook()

@app.route('/delete/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete(id):
    pass

@app.route('/update/<audioFileType>/<audioFileID>', methods=['PUT'])
def update(id):
    pass

@app.route('/<audioFileType>/<audioFileID>', methods=['GET'])
def getAPI(id):
    pass


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
