from langchain_core.tools import tool
import requests

from config import Config


API_HEADERS = Config.API_HEADERS
HOTEL_API_URL = Config.HOTEL_API_URL


@tool
def list_meals():
    """list all available meals available in the restaurants"""
    return requests.get(HOTEL_API_URL + "/api/meals/", headers=API_HEADERS).text


@tool
def list_restaurants():
    """list all available restaurants in the hotel available for reservation"""
    return requests.get(HOTEL_API_URL + "/api/restaurants/", headers=API_HEADERS).text
