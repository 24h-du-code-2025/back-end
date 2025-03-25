from langchain_core.tools import tool


from config import Config
from utils.utils_weather import get_weather_info


@tool
def get_weather(city):
    """Use this to predict weather information for a given city"""
    return get_weather_info(Config.OPEN_WEATHER_API_KEY, city)
