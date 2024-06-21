from flask import Flask, jsonify, render_template, request, Response
import requests
from flask_cors import CORS
from typing import Tuple, Union

app = Flask(__name__)
CORS(app)

BACKEND_ENDPOINT = 'http://localhost:5000'

@app.route('/check_backend')
def check_backend() -> Tuple[str, int]:
    """
    Endpoint to check the status of the backend server.
    Returns:
        Tuple[str, int]: A tuple containing a message indicating the server status and an HTTP status code.
    """

    try:
        response = requests.get(f'{BACKEND_ENDPOINT}/health')
        if response.status_code == 200:
            return 'Back end server is running.', 200
        else:
            return 'Back end server is not running.', 500
    except requests.exceptions.ConnectionError:
        return 'Unable to connect to back end server.', 500
    
@app.route('/')
def index() -> str:
    """
    Render the index.html template.
    """

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)