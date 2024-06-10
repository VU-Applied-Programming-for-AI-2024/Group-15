from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config import config

load_dotenv()

app = Flask(__name__)
CORS(app)

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

@app.route('/')
def home():
    return jsonify(message="Hello, Flask!")

@app.route('/api/test')
def test_api():
    return jsonify(status='success', message='API is working')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
