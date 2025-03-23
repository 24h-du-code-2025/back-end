from os import getenv

import requests
from dotenv import dotenv_values
from flask import Flask, request
from flask_socketio import SocketIO, emit
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field, validator
from pymongo import MongoClient

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Dict, Optional
from typing_extensions import TypedDict

from utils import get_weather_info, extract_events

load_dotenv()
HOTEL_API_URL = getenv("HOTEL_API_URL")
HOTEL_API_KEY = getenv("HOTEL_API_KEY")
API_HEADERS = {"Authorization": f"Token {HOTEL_API_KEY}"}

if getenv("LLM_MODEL") == "CHATGPT":
    model = ChatOpenAI(model="gpt-4o-mini")
elif  getenv("LLM_MODEL") == "CHATGPT_BLING":
    model = ChatOpenAI(model="gpt-4o")

OPEN_WEATHER_API_KEY = getenv('OPEN_WEATHER_API_KEY')


@tool
def get_weather(city):
    """Use this to predict weather information for a given city"""
    return get_weather_info(OPEN_WEATHER_API_KEY, city)


@tool
def get_client(client_id):
    """get information about client by its id"""
    return requests.get(HOTEL_API_URL + f"/api/clients/{client_id}/", headers=API_HEADERS).text



class UpdateClientInfo(BaseModel):
    client_id: int = Field(description="client id")
    name: str = Field(description="client name")
    phone_number: str = Field(description="client phone number")
    room_number: str = Field(description="client room number")
    special_requests: str = Field(description="client special requests")


@tool
def update_client(update_info: UpdateClientInfo):
    """update client information"""
    body_parameters = update_info.dict()
    client_id = update_info.client_id
    if 'client_id' in body_parameters:
        del body_parameters['client_id']
    return requests.update(
        HOTEL_API_URL + f"/api/clients/{client_id}/",
        headers=API_HEADERS,
        json=body_parameters
    ).text
    

@tool
def delete_client(client_id):
    """delete client by its id"""
    requests.delete(HOTEL_API_URL + f"/api/clients/{client_id}/", headers=API_HEADERS)




class ClientModel(BaseModel):
    name: str = Field(description="First and last name of the client")
    phone_number: str = Field(description="phone number of the client")
    room_number: Optional[str] = Field(description="the number of the room")
    special_requests: Optional[str] = Field(description="any additional info or special request about the client and his reservation",
                                  examples=["I need a double bed", "I will left at 10 o clock"])

@tool(args_schema=ClientModel)
def create_client(
        name: str,
        phone_number: str,
        room_number: str = None,
        special_requests: str = None
):
    """register a new client in the hotel"""
    return requests.post(HOTEL_API_URL + "/api/clients/", data={
    "name": name,
    "phone_number": phone_number,
    "room_number": room_number,
    "special_requests": special_requests
}, headers=API_HEADERS).text

@tool()
def search_client(
        search: str,
):
    """search a client by his name or phone number use this tool to check if a user is already registered """
    return requests.get(HOTEL_API_URL + "/api/clients/", params={
    "search": search,
}, headers=API_HEADERS).text


@tool
def get_spas():
    """list all available spas arround the hotel"""
    return requests.get(HOTEL_API_URL+"/api/spas/", headers=API_HEADERS).text


@tool
def list_meals():
    """list all available meals available in the restaurants"""
    return requests.get(HOTEL_API_URL+"/api/meals/", headers=API_HEADERS).text


@tool
def list_reservations():
    """list all reservations in the restaurants"""
    return requests.get(HOTEL_API_URL+"/api/reservations/", headers=API_HEADERS).text


def get_available_restaurant_ids() -> List[int]:
    """Fetch the list of available restaurant IDs from the API"""
    response = requests.get(f"{HOTEL_API_URL}/api/restaurants/", headers=API_HEADERS)
    if response.status_code == 200:
        data = response.json()
        return [restaurant["id"] for restaurant in data["results"]]
    return []


AVAILABLE_RESTAURANT_IDS = get_available_restaurant_ids()

"""
    "id": 0,
    "client": 0,
    "restaurant": 0,
    "date": "2019-08-24",
    "meal": 0,
    "number_of_guests": 1,
    "special_requests": "string"
"""
class ReservationDesplayInfo(BaseModel):
    restaurant_name: str = Field(description="the name of the restaurant")
    restaurant_location: str = Field(description="address of the restaurant")
    reservation_date: str = Field(description="the date and hour of the reservation")
    meal: str = Field(description="the name of the meal reserved")
    number_of_guests: int = Field(description="the number of guests for the reservation")
    special_requests: Optional[str] = Field(description="Other informations about the reservation")

@tool
def display_reservation_data(
        reservation: ReservationDesplayInfo
):
    """When a reservation is created or the user ask about the details of a reservation, always respond using this tool"""
    session = database.sessions.find_one({"sid": request.sid})
    print(session["token"])
    add_structured_message("reservation_details", reservation.dict())
    return "__end__"

class ReservationInfo(BaseModel):
    date: int = Field(description="the date for the reservation")
    meal: int = Field(description="the id of the meal in the hotel api")
    restaurant: int = Field(description="the id of the restaurant in the hotel api")
    number_of_guests: int = Field(description="the number of guests for the reservation")
    special_requests: str = Field(description="any additional info or special request about the reservation", examples=["next to the entrance", "near the toilets", "2 persons are vegetarians"])

    @validator("restaurant")
    def validate_restaurant_id(cls, value):
        """Check if the restaurant ID is in the available list"""
        if value not in AVAILABLE_RESTAURANT_IDS:
            raise ValueError(f"Restaurant with id {value} does not exist.")
        return value



@tool
def add_reservation(reservation: ReservationInfo):
    """Create a restaurant reservation"""
    return requests.post(HOTEL_API_URL + "/api/reservations/", json=reservation.dict(), headers=API_HEADERS).text


@tool
def get_reservation(reservation_id: int):
    """Get information about a restaurant reservation"""
    return requests.get(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", headers=API_HEADERS).text


class GetReservationsParams(BaseModel):
    client: Optional[int] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    meal: Optional[int] = None
    page: Optional[int] = None
    restaurant: Optional[int] = None


@tool
def get_reservations(params: GetReservationsParams):
    """Get information about client reservations"""
    params_dict = {k: v for k, v in params.dict().items() if v is not None}
    return requests.post(HOTEL_API_URL + f"/api/reservations", params=params_dict, headers=API_HEADERS).text


class UpdateReservationsParams(BaseModel):
    client: Optional[int] = None
    restaurant: Optional[int] = None
    date: Optional[str] = None
    meal: Optional[int] = None
    number_of_guests: Optional[int] = None
    special_requests: Optional[str] = None


@tool
def update_reservation(reservation_id: int, params: UpdateReservationsParams):
    """Update reservation information"""
    return requests.put(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", params=params, headers=API_HEADERS).text


class PatchReservationsParams(BaseModel):
    client: Optional[int] = None
    restaurant: Optional[int] = None
    date: Optional[str] = None
    meal: Optional[int] = None
    number_of_guests: Optional[int] = None
    special_requests: Optional[str] = None


@tool
def patch_reservation(reservation_id: int, params: PatchReservationsParams):
    """Partially update reservation information"""
    return requests.patch(HOTEL_API_URL + f"/api/reservations/{reservation_id}/", params=params, headers=API_HEADERS).text


@tool
def delete_reservation(reservation_id: int):
    """list all available spas arround the hotel"""
    return requests.delete(HOTEL_API_URL + f"/api/reservations/{reservation_id}", headers=API_HEADERS).text
    


@tool
def list_restaurants():
    """list all available restaurants in the hotel available for reservation"""
    return requests.get(HOTEL_API_URL+"/api/restaurants/", headers=API_HEADERS).text


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
    """When the user ask details about a spa and there is only one spa to display, always respond using this tool"""
    session = database.sessions.find_one({"sid": request.sid})
    print(session["token"])
    add_structured_message("spa_details", spa)
    return "__end__"


@tool
def display_spa_list(
        spas: List[SpaInfo]
):
    """When the user ask about spas and there is a list to display, always respond using this tool"""
    session = database.sessions.find_one({"sid": request.sid})
    print(session["token"])
    add_structured_message("spa_list", spas)
    return "__end__"


class EventInfo(TypedDict):
    title: Optional[str]
    date: Optional[str]
    category: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    link: Optional[str]
    

@tool
def display_events(
        events: List[EventInfo]
):
    """When the user ask details about upcoming events or news in Le Mans, always respond using this tool"""
    print("show_events")
    add_structured_message("events_list", events)
    return "__end__"


@tool
def get_events():
    """List upcoming events and news in Le Mans"""
    print("get_events")
    return extract_events()


tools = [
    get_weather,
    get_spas,
    display_spa_data,
    display_spa_list,
    list_meals,
    list_reservations,
    list_restaurants,
    add_reservation,
    get_reservation,
    get_reservations,
    update_reservation,
    patch_reservation,
    delete_reservation,
    get_events,
    display_events,
    get_client,
    update_client,
    delete_client,
    create_client,
    search_client,
    display_reservation_data
]


def call_agent(user_input: str, session):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},
                              {"configurable": {"thread_id": session["_id"]}}):
        for value in event.values():
            if value["messages"][-1].content == '__end__':
                return
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

## client account
To make any reservation or request, the user must be linked to a user account created via the create_client tool or found via the search_client tool.

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

# def prompt_user(question, answers):
