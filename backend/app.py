import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import config

app = Flask(__name__)
env = os.getenv('FLASK_ENV', 'development')  
app.config.from_object(config[env])
CORS(app)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello from Flask!')

if __name__ == '__main__':
    app.run()