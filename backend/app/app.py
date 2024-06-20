from flask import Flask
from flask_cors import CORS
import logging


app = Flask(__name__)
CORS(app) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)