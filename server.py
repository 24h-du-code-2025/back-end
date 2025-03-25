import os
from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import whisper

from config import Config
from utils import call_agent, convert_mp3_to_wav


speech_to_text_model = whisper.load_model("base")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins='*')

config = dotenv_values(".env")
mongodb_client = MongoClient(Config.ATLAS_URI)
database = mongodb_client[Config.DB_NAME]

connected_users = []


@app.route("/convert-speech-to-text")
def convert_speech_to_text():
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio']
    
    if not audio_file.filename.endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        return jsonify({"error": "Invalid file format. Please upload an MP3, WAV, M4A, or OGG file."}), 400

    temp_audio_path = f"temp_{audio_file.filename}"
    audio_file.save(temp_audio_path)

    if temp_audio_path.endswith('.mp3'):
        wav_path = convert_mp3_to_wav(temp_audio_path)

    try:
        result = speech_to_text_model.transcribe(wav_path)
        os.remove(wav_path)
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@sio.on('chat')
def handle_chat(data):
    session = database.sessions.find_one({"sid": request.sid})

    if "message" not in data:
        return

    add_message("user", data["message"])
    call_agent(data["message"], session)


@sio.on('connect')
def handle_connect(auth=None):
    if auth is None or "token" not in auth:
        return
    session = database.sessions.find_one({"token": auth["token"]})
    if session is None:
        database.sessions.insert_one({"token": auth["token"], "history": []})
        session = database.sessions.find_one({"token": auth["token"]})

    session["sid"] = request.sid
    update_session(session)
    send_history(session)


def add_message(from_name, content):
    session = database.sessions.find_one({"sid": request.sid})
    session["history"].append({
        "from": from_name,
        "type": "message",
        "content": content
    })
    update_session(session)
    send_history(session)


def add_structured_message(message_type, content):
    session = database.sessions.find_one({"sid": request.sid})
    session["history"].append({
        "from": "agent",
        "type": message_type,
        "content": content
    })
    update_session(session)
    send_history(session)


def update_session(session):
    database["sessions"].update_one({"_id": session["_id"]}, {"$set": session})


def send_history(session):
    emit('update_history', session["history"], to=session["sid"])


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
