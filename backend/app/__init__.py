from flask import Flask, jsonify
from flask_cors import CORS
from config import config

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(config)

app = create_app()