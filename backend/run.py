from flask import Flask
from waitress import serve
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=int(os.getenv("WEBSITE_PORT", 8000)))