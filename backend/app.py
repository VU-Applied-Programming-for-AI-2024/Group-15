from flask import Flask, jsonify
from flask_cors import CORS
import os
from config import config

app = Flask(__name__)
CORS(app)

# Determine which environment to use
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

@app.route('/')
def home():
    return jsonify(message="Hello, Flask!")

@app.route('/api/test')
def test_api():
    return jsonify(status='success', message='API is working')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
