from flask import Flask
from flask_cors import CORS
import logging
from routes import register_routes
import json
from bson import ObjectId

def create_app():

    app = Flask(__name__)
    CORS(app)
    logging.basicConfig(level=logging.INFO)
    register_routes(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

app.json_encoder = JSONEncoder