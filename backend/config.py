import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secure_key'
    EXERCISE_API_KEY = os.environ.get('EXERCISE_API_KEY') or '4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh'
    BASE_URL = os.environ.get('BASE_URL') or "https://zylalabs.com/api/392/exercise+database+api"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'

class ProductionConfig(Config):
    ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}