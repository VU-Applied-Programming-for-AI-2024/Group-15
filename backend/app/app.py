from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Hardcoded API connection details
API_ENDPOINT = "https://api.example.com/data"
API_KEY = "your_api_key_here"

def fetch_api_data():
    """Fetch data from the external API."""
    response = requests.get(API_ENDPOINT, headers={"Authorization": f"Bearer {API_KEY}"})

    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch data from the API"}, response.status_code

@app.route('/api_data', methods=['GET'])
def get_api_data():
    data, status_code = fetch_api_data()
    return jsonify(data), status_code

if __name__ == '__main__':
    app.run(debug=True)


