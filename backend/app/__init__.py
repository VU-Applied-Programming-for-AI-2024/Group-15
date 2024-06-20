from flask import Flask
from flask_cors import CORS
import logging
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS

    logging.basicConfig(level=logging.INFO)
    from .routes import register_routes
    register_routes(app)

    return ap