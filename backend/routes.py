from flask import jsonify, request
import requests
import os
from typing import List, Any, Union, Dict
from dotenv import load_dotenv, find_dotenv
from utils.crud_operations_azure import server_crud_operations
import json
import openai
import logging 
import uuid

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_KEY = os.environ.get("OPENAI_KEY")
openai.api_key = os.getenv("OPENAI_KEY")
API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_KEY = os.environ.get("EXERCISE_API_KEY")
BASE_URL = os.environ.get("API_ENDPOINT")
OPENAI_KEY = os.environ.get("OPENAI_KEY")


def create_schedule_with_openai(age, gender, weight, goal, days, available_time):
    try:
        prompt = f"""
        Create a detailed workout schedule in JSON format for a {age} year old {gender} who weighs {weight} kg and has a goal of {goal}. 
        The schedule should be distributed over {len(days)} days ({', '.join(days)}) with each session being {available_time} minutes long. 
        Each day's schedule should include exercises with sets and reps that fit within the available time per session, considering that each rep takes 3 seconds and 60 seconds rest between each set.
        The output should only be a valid JSON object, no additional text or formatting. Example format:
        {{
            "Day 1": {{
                "Muscle_Group": "Chest and Arms",
                "Exercises": {{
                    "Exercise 1": {{"Sets": 3, "Reps": 10}},
                    "Exercise 2": {{"Sets": 3, "Reps": 10}}
                }}
            }},
            "Day 2": {{
                "Muscle_Group": "Back and Shoulders",
                "Exercises": {{
                    "Exercise 1": {{"Sets": 3, "Reps": 10}},
                    "Exercise 2": {{"Sets": 3, "Reps": 10}}
                }}
            }}
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        structured_data = response.choices[0].message['content'].strip()
        logger.info(f"Structured data from OpenAI: {structured_data}")

        json_data = json.loads(structured_data)
        return json_data

    except json.JSONDecodeError as json_err:
        logger.error(f"JSON decode error: {json_err}")
        raise ValueError("Invalid JSON response from OpenAI")
    except Exception as e:
        logger.error(f"Error in parsing exercise response: {str(e)}")
        raise

def search_exercises(user_input, bodypart, equipment):
    endpoint = f"{BASE_URL}/310/list+exercise+by+body+part"
    params = {'bodyPart': bodypart}
    exercises, status_code = fetch_api_data(endpoint, params)
    
    if status_code != 200:
        return {"error": "Failed to fetch exercises"}, status_code

    filtered_exercises = [
        exercise for exercise in exercises
        if (user_input.lower() in exercise['name'].lower() or 
            user_input.lower() in exercise['target'].lower()) and 
        (equipment.lower() in exercise['equipment'].lower())
    ]

    return filtered_exercises, 200

def fetch_api_data(endpoint, params=None):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch data from the API!"}, response.status_code

def register_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Exercise Database API! FElix is the best "

    @app.route('/list_of_body_parts', methods=['GET'])
    def list_of_body_parts():
        endpoint = f"{BASE_URL}/309/list+of+body+parts"
        data, status_code = fetch_api_data(endpoint)
        return jsonify(data), status_code

    @app.route('/exercise_by_id', methods=['GET'])
    def exercise_by_id():
        exercise_id = request.args.get('id', '14')
        endpoint = f"{BASE_URL}/1004/exercise+by+id"
        params = {'id': exercise_id}
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    @app.route('/list_of_equipment', methods=['GET'])
    def list_of_equipment():
        endpoint = f"{BASE_URL}/2082/list+of+equipment"
        data, status_code = fetch_api_data(endpoint)
        return jsonify(data), status_code

    @app.route('/search_exercises', methods=['GET'])
    def search_exercises_route():
        user_input = request.args.get('user_input', '')
        bodypart = request.args.get('bodypart', '')
        equipment = request.args.get('equipment', '')

        exercises, status_code = search_exercises(user_input, bodypart, equipment)
        return jsonify(exercises), status_code
    
    @app.route('/get_favorites', methods=['GET'])
    def get_favorites_by_email():
        try:
            email = request.args.get('email')
            
            if not email:
                return jsonify({"status": "error", "message": "Email parameter is required"}), 400
            
            favorites = server_crud_operations(
                operation="read",
                collection_name="favorites",
                key="email",
                value=email
            )
            
            if favorites:
                return jsonify({"status": "success", "favorites": favorites}), 200
            else:
                return jsonify({"status": "error", "message": "No favorites found for the provided email"}), 404
        
        except Exception as e:
            logging.error(f"Error in get_favorites_by_email: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
        
    @app.route('/add_to_favorites', methods=['POST'])
    def add_to_favorites():
        try:
            data = request.json
            email = data['email']
            schedule_name = data['scheduleName']
            schedule = data['schedule']

            # Insert into the favorites collection
            favorite = {
                "_id": email + schedule_name,
                "email": email,
                "schedule_name": schedule_name,
                "schedule": schedule
            }
            server_crud_operations(
                operation="insert",
                json_data={"favorite": favorite},
                collection_name="favorites"
            )

            return jsonify({"status": "success", "message": "Schedule added to favorites successfully"}), 200
        except Exception as e:
            logger.error(f"Error adding schedule to favorites: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/create-schedule', methods=['POST'])
    def create_schedule():
        try:
            data = request.get_json()
            app.logger.info(f"Received data: {data}")
            
            age = int(data.get('age'))
            gender = data.get('gender')
            weight = int(data.get('weight'))
            goal = data.get('goal')
            days = data.get('days')
            available_time_per_session = int(data.get('available_time'))

            schedule = create_schedule_with_openai(age, gender, weight, goal, days, available_time_per_session)

            # Generate unique string ID for the schedule
            schedule_id = str(uuid.uuid4())
            schedule["_id"] = schedule_id

            # Store the schedule in the database
            inserted_id = server_crud_operations(
                operation="insert",
                json_data=schedule,
                collection_name="Schedules"
            )

            return jsonify({"status": "success", "schedule_id": schedule_id, "schedule": schedule}), 200
        except Exception as e:
            app.logger.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get-schedule/<schedule_id>', methods=['GET'])
    def get_schedule(schedule_id):
        try:
            logger.info(f"Received request to get schedule with id: {schedule_id}")
            result = server_crud_operations(
                operation="read",
                collection_name="Schedules",  # Ensure collection name matches the one used in the insert operation
                value=schedule_id
            )
            
            if result:
                logger.info(f"Found a document with _id {schedule_id}: {result}")
                return jsonify({"status": "success", "schedule": result['schedule']}), 200
            else:
                logger.info(f"No document found with _id {schedule_id}")
                return jsonify({"status": "error", "message": "Schedule not found"}), 404
        except Exception as e:
            logger.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500