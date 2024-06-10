from flask import Flask, jsonify
from flask_cors import CORS
from config import config

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(config)

    @app.route('/')
    def home():
        return jsonify(message="Hello, Flask!")

    @app.route('/api/test')
    def test_api():
        return jsonify(status='success', message='API is working')

    return app

app = create_app()