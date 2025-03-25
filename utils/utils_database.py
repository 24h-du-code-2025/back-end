from flask import request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient


from config import Config


mongodb_client = MongoClient(Config.ATLAS_URI)
database = mongodb_client[Config.DB_NAME]


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
