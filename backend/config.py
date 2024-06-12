import os

class DevelopmentConfig:
    DEBUG = True

class Config:
    EXERCISE_API_KEY = os.environ.get('EXERCISE_API_KEY') or '4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh'
    BASE_URL = os.environ.get('BASE_URL') or "https://zylalabs.com/api/392/exercise+database+api"
    DEBUG = False # Set this to False in production
    TESTING = False

config = Config()

