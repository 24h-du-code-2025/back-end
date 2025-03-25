from langchain_core.tools import tool
import requests
from typing import List

from config import Config
from model import SpaModel
from utils import add_structured_message


API_HEADERS = Config.API_HEADERS
HOTEL_API_URL = Config.HOTEL_API_URL


@tool
def get_spas():
    """list all available spas arround the hotel"""
    return requests.get(HOTEL_API_URL+"/api/spas/", headers=API_HEADERS).text


@tool
def display_spa_data(
        spa: SpaModel
):
    """When the user ask details about a spa and there is only one spa to display, always respond using this tool"""
    add_structured_message("spa_details", spa)
    return "__end__"


@tool
def display_spa_list(
        spas: List[SpaModel]
):
    """When the user ask about spas and there is a list to display, always respond using this tool"""
    add_structured_message("spa_list", spas)
    return "__end__"
