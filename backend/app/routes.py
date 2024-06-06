from flask import Blueprint, request, jsonify, render_template
import requests
import os

main = Blueprint('main', __name__)

API_KEY = os.environ.get('EXERCISE_API_KEY', '4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh')
BASE_URL = "https://zylalabs.com/api/392/exercise+database+api"

def get_api_data(endpoint, params=None):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/api/body-parts', methods=['GET'])
def list_body_parts():
    data = get_api_data("309/list+of+body+parts")
    return jsonify(data)

@main.route('/api/exercises', methods=['GET'])
def list_exercises_by_body_part():
    body_part = request.args.get('bodyPart', 'cardio')
    data = get_api_data("310/list+exercise+by+body+part", params={'bodyPart': body_part})
    return jsonify(data)

@main.route('/api/target-muscles', methods=['GET'])
def list_target_muscles():
    data = get_api_data("311/list+of+target+muscles")
    return jsonify(data)

@main.route('/api/exercises-by-muscle', methods=['GET'])
def list_exercises_by_target_muscle():
    target = request.args.get('target', 'biceps')
    data = get_api_data("312/list+by+target+muscle", params={'target': target})
    return jsonify(data)
