from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    return app 


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
