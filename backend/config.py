import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secure_key'
    EXERCISE_API_KEY = os.environ.get('EXERCISE_API_KEY') or '4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh'
    BASE_URL = os.environ.get('BASE_URL') or "https://zylalabs.com/api/392/exercise+database+api"
    DEBUG = True  # Set this to True for simplicity
    TESTING = False

config = Config()