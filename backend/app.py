from flask import Flask, jsonify
from flask_cors import CORS
import os
from config import config

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

