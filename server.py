from dotenv import dotenv_values
from flask import Flask, request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins='*')


config = dotenv_values(".env")
mongodb_client = MongoClient(config["ATLAS_URI"])
database = mongodb_client[config["DB_NAME"]]


connected_users = []


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@sio.on('chat')
def handle_chat(data):
    session = database.sessions.find_one({"sid": request.sid})

    if "message" not in data:
        return
    print('received message: ')
    print(data)
    print(data["message"])



    session["history"].append({
        "from": "user",
        "message": data["message"]
    })
    update_session(session)
    send_history(session)


@sio.on('connect')
def handle_connect(auth = None):
    print(auth)
    if auth is None or "token" not in auth:
        return
    session = database.sessions.find_one({"token": auth["token"]})
    if session is None:
        database.sessions.insert_one({"token": auth["token"], "history": []})
        session = database.sessions.find_one({"token": auth["token"]})

    session["sid"] = request.sid
    update_session(session)
    send_history(session)
    print(session)


def update_session(session):
    database["sessions"].update_one({"_id": session["_id"]}, { "$set": session })


def send_history(session):
    emit('update_history', session["history"],  to=session["sid"])

# def prompt_user(question, answers):

