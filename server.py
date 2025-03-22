from os import getenv

import requests
from dotenv import dotenv_values
from flask import Flask, request
from flask_socketio import SocketIO, emit
from langchain_core.messages import AIMessage
from pymongo import MongoClient


from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Dict, TypedDict

load_dotenv()
HOTEL_API_URL = getenv("HOTEL_API_URL")
HOTEL_API_KEY = getenv("HOTEL_API_KEY")
API_HEADERS={"Authorization":f"Token {HOTEL_API_KEY}"}

if getenv("LLM_MODEL")== "CHATGPT":
    model = ChatOpenAI(model="gpt-4o-mini")


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")

@tool
def create_client(phone):
    """register a user"""


@tool
def get_spas():
    """list all available spas arround the hotel"""
    return requests.get(HOTEL_API_URL+"/api/spas", headers=API_HEADERS).text

@tool
def list_meals():
    """list all available meals available in the restaurants"""
    return requests.get(HOTEL_API_URL+"/api/meals", headers=API_HEADERS).text

@tool
def list_reservations():
    """list all reservations in the restaurants"""
    return requests.get(HOTEL_API_URL+"/api/reservations", headers=API_HEADERS).text

@tool
def add_reservation():
    """list all available spas arround the hotel"""

@tool
def get_reservation():
    """list all available spas arround the hotel"""

@tool
def delete_reservation():
    """list all available spas arround the hotel"""

@tool
def list_restaurants():
    """list all available restaurants in the hotel available for reservation"""
    return requests.get(HOTEL_API_URL+"/api/restaurants", headers=API_HEADERS).text



class SpaInfo(TypedDict):
    name: str
    description: str
    location: str
    phone_number: str
    email: str
    opening_hours: str


@tool
def display_spa_data(
       spa: SpaInfo
):
    """When the user ask details about a spa, always respond using this tool"""
    print("show_spa_data")
    session = database.sessions.find_one({"sid": request.sid})
    print(session["token"])
    add_structured_message("spa_details",spa)

@tool
def display_spa_list(
        spas: List[SpaInfo]
):
    """When the user ask details about a spa, always respond using this tool"""
    print("show_spa_data")
    session = database.sessions.find_one({"sid": request.sid})
    print(session["token"])
    add_structured_message("spa_list",spas)


tools = [
    get_weather,
    get_spas,
    display_spa_data,
    display_spa_list,
    list_meals,
    list_reservations,
    list_restaurants
]


def call_agent(user_input: str, session):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": session["_id"]}}):
        for value in event.values():
            if type(value["messages"][-1]) == AIMessage and value["messages"][-1].content != '':
                add_message("agent", value["messages"][-1].content)



memory = MemorySaver()


sys_prompt = """
# System Prompt: Hotel Concierge AI

You are an AI Hotel Concierge designed to assist guests during their stay. Your role is to provide helpful, courteous, and efficient service while maintaining the professionalism expected of a high-quality hotel concierge.

## Core Responsibilities

Your primary function is to help guests with the following services:

1. **Restaurant Information**
   - Provide a complete list of restaurants available in the hotel
   - Share detailed information about each restaurant including cuisine type, opening hours, and ambiance
   - Answer questions about specific menu items and special dietary accommodations

2. **Menu Assistance**
   - List available dishes at any hotel restaurant
   - Describe dishes, ingredients, and preparation methods
   - Highlight chef's specialties and seasonal offerings
   - Provide information about pricing

3. **Restaurant Reservations**
   - Help guests make restaurant reservations
   - Check availability for specific dates and times
   - Confirm reservation details
   - Process special requests (e.g., birthday celebrations, seating preferences)
   - Handle cancellations and modifications to existing reservations

4. **Spa Services**
   - Provide information about spa facilities within the hotel
   - Recommend nearby spa options with relevant details
   - Share information about treatments, pricing, and availability
   - Assist with directions to spa locations

## Interaction Guidelines

- **Language Adaptation**: Always respond in the same language used by the guest. You are fluent in multiple languages and should match the guest's preferred language.

- **Tone and Style**: Maintain a professional, warm, and helpful demeanor. Your communication should be:
  - Courteous and respectful
  - Clear and concise
  - Patient and understanding
  - Appropriately formal without being stiff

- **Problem Solving**: If you cannot fulfill a request directly, offer alternatives or escalation paths to human staff when appropriate.

- **Personalization**: Remember guest preferences when mentioned and use this information to provide personalized recommendations.

## Knowledge Base

You have access to current information about:
- All hotel restaurants, their menus, and availability
- Local spa facilities and services
- Special events and promotions

## Privacy and Data Handling

- Respect guest privacy and confidentiality
- Only collect information necessary to fulfill requests
- Do not store personal information beyond the current conversation

## Example Interactions

**Restaurant Recommendations**:
Guest: "What restaurants do you have in the hotel?"
Response: [List all hotel restaurants with brief descriptions]

**Menu Inquiries**:
Guest: "What dishes does your Italian restaurant offer?"
Response: [Provide menu items from the Italian restaurant]

**Making Reservations**:
Guest: "I'd like to book a table for 4 at 8pm tomorrow."
Response: [Check availability and confirm or suggest alternatives]

**Spa Information**:
Guest: "Where can I find a good spa nearby?"
Response: [Provide information about hotel spa and nearby options]

Always aim to enhance the guest experience through helpful, accurate, and pleasant service.

## Structured response
Some data can be returned to the user using the corresponding tool,
if a tool is available to return structured data, use it then respond with "Here is your response"
"""


graph = create_react_agent(model, tools=tools, checkpointer=memory, prompt=sys_prompt)



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

    add_message( "user", data["message"])

    if data["message"] == "test":
        emit('ask_question', {
            "question": "comment ça va",
            "responses": [
              {
                "value": "good",
                "label": "Je vais bien",
                "type": "info"
              },
              {
                "value": "bad",
                "label": "Je vais pas bien",
                "type": "danger"
              }
            ]
          }
        , to=session["sid"])
        return

    call_agent(data["message"], session)


@sio.on('connect')
def handle_connect(auth = None):
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
    database["sessions"].update_one({"_id": session["_id"]}, { "$set": session })


def send_history(session):
    emit('update_history', session["history"],  to=session["sid"])

# def prompt_user(question, answers):


