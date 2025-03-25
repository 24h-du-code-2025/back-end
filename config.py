from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    
    ATLAS_URI = getenv("ATLAS_URI")
    DB_NAME = getenv("DB_NAME")
    
    HOTEL_API_URL = getenv("HOTEL_API_URL"),
    HOTEL_API_KEY = getenv("HOTEL_API_KEY")
    OPEN_WEATHER_API_KEY = getenv("OPEN_WEATHER_API_KEY"),
    API_HEADERS = {"Authorization": f"Token {HOTEL_API_KEY}"},
    
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    
    LLM_MODEL = getenv("LLM_MODEL")
