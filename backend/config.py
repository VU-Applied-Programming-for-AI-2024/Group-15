import os

class DevelopmentConfig:
    DEBUG = True

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secure_key'
    EXERCISE_API_KEY = os.environ.get('EXERCISE_API_KEY') or 'default_key'
    BASE_URL = os.environ.get('BASE_URL') or "https://example.com/api"
    DEBUG = True  # Set this to False in production
    TESTING = False

config = Config()

