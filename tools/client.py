from langchain_core.tools import tool
import requests
from typing import Optional

from config import Config
from model import CreateClientModel, UpdateClientModel


API_HEADERS = Config.API_HEADERS
HOTEL_API_URL = Config.HOTEL_API_URL


# @tool
# def create_client(client: CreateClientModel):
#     """register a new client in the hotel"""
#     return requests.post(HOTEL_API_URL + "/api/clients/", json=client.dict(), headers=API_HEADERS).text

@tool(args_schema=CreateClientModel)
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


@tool
def get_clients(page: Optional[int], term: Optional[str]):
    """Searches for clients using a provided search term"""
    return requests.get(HOTEL_API_URL + f"/api/clients/", params={"page": page, term: "term"}, headers=API_HEADERS).text


@tool
def get_client(client_id: int):
    """get information about client by its id"""
    return requests.get(HOTEL_API_URL + f"/api/clients/{client_id}/", headers=API_HEADERS).text


@tool()
def search_client(
        search: str,
):
    """search a client by his name or phone number use this tool to check if a user is already registered """
    return requests.get(HOTEL_API_URL + "/api/clients/", params={
    "search": search,
}, headers=API_HEADERS).text


@tool
def update_client(client_id: int, update_info: UpdateClientModel):
    """update client information"""
    return requests.put(
        HOTEL_API_URL + f"/api/clients/{client_id}/",
        headers=API_HEADERS,
        json=update_info.dict()
    ).text
    

@tool
def delete_client(client_id: int):
    """delete client by its id"""
    requests.delete(HOTEL_API_URL + f"/api/clients/{client_id}/", headers=API_HEADERS)
