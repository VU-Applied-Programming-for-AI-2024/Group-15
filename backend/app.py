from flask import Flask, request
from flask_cors import CORS
import logging
from routes import register_routes



def create_app():
    app = Flask(__name__)
    CORS(app)
    logging.basicConfig(level=logging.INFO)
    register_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)