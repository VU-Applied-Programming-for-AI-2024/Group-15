import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    API_ENDPOINT = os.environ.get("API_ENDPOINT")
    EXERCISE_API_KEY = os.environ.get("EXERCISE_API_KEY")