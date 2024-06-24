from flask import jsonify, request
import requests
import os
from typing import List, Any, Union, Dict
from dotenv import load_dotenv, find_dotenv
from models.day import Day
from models.bodypart import BodyPart
from models.schedule import Schedule
from models.exercise import Exercise
from models.workout_exercise import WorkoutExercise
from models.workout import Workout
from utils.crud_operations_azure import server_crud_operations
import re
from bson import ObjectId
import json
from models.bodypart import MuscleGroupDistributor
import concurrent.futures
import logging

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_KEY = "4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh"
BASE_URL = "https://zylalabs.com/api/392/exercise+database+api"

class CustomScheduleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BodyPart):
            return obj.value  # List of strings
        elif isinstance(obj, Exercise):
            return {
                'bodyPart': obj.body_part,
                'equipment': obj.equipment,
                'gifUrl': obj.gif_url,
                'id': obj.exercise_id,
                'name': obj.name,
                'target': obj.target
            }
        elif isinstance(obj, WorkoutExercise):
            return {
                'exercise': self.default(obj.exercise),
                'sets': obj.sets,
                'reps': obj.reps
            }
        elif isinstance(obj, Workout):
            return {
                'exercises': [self.default(ex) for ex in obj.exercises]
            }
        elif isinstance(obj, Schedule):
            return {
                day.name: self.default(workout)
                for day, workout in obj.schedule.items()
            }
        return super().default(obj)


def treat_gender_data(gender):
    if gender == "other":
        gender = "female"
    return gender

def treat_muscles_data (muscles)->List[BodyPart]:
     # Change the muscles into BodyParts objects
    muscle_list: List[BodyPart] = []
    for muscle in muscles:
        if muscle == "back":
            muscle_list.append(BodyPart.BACK)
        if muscle == "cardio":
            muscle_list.append(BodyPart.CARDIO)
        if muscle == "chest":
            muscle_list.append(BodyPart.CHEST)
        if muscle == "lower arms":
            muscle_list.append(BodyPart.LOWER_ARMS)
        if muscle == "lower legs":
            muscle_list.append(BodyPart.LOWER_LEGS)
        if muscle == "neck":
            muscle_list.append(BodyPart.NECK)
        if muscle == "shoulders":
            muscle_list.append(BodyPart.SHOULDERS)
        if muscle == "upper arms":
            muscle_list.append(BodyPart.UPPER_ARMS)
        if muscle == "upper legs":
            muscle_list.append(BodyPart.UPPER_LEGS)
        if muscle == "waist":
            muscle_list.append(BodyPart.WAIST)
        
    return muscle_list

def search_exercises(user_input, bodypart, equipment):
    endpoint = f"{BASE_URL}/310/list+exercise+by+body+part"
    params = {'bodyPart': bodypart}
    exercises, status_code = fetch_api_data(endpoint, params)
    
    if status_code != 200:
        return {"error": "Failed to fetch exercises"}, status_code

    filtered_exercises = [
        exercise for exercise in exercises
        if (user_input.lower() in exercise['name'].lower() or 
            user_input.lower() in exercise['description'].lower()) and 
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

def fetch_api_data_async(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the API!"}

def call_external_api(api_data):
    try:
        endpoint = f"{API_ENDPOINT}/create-routine"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        logging.debug(f"Calling external API at {endpoint} with data: {api_data}")
        response = requests.post(endpoint, headers=headers, json=api_data)
        
        logging.debug(f"External API response status: {response.status_code}")
        logging.debug(f"External API response data: {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": False, "message": "Failed to create routine"}
    except Exception as e:
        logging.error(f"Error calling external API: {str(e)}")
        return {"status": False, "message": str(e)}


def process_api_response(api_response):
    routine = {}
    for day_info in api_response['routine']:
        day_name = extract_day(day_info)  # Extract day from day_info string
        exercises_reps = extract_exercises_reps(day_info)  # Extract exercises and reps
        routine[day_name] = exercises_reps
    return routine

def extract_day(day_info):
    # Example: "Day 1: Upper Body - Triceps Focus"
    return day_info.split(":")[0].strip()

def extract_exercises_reps(day_info):
    # Example: "1. Barbell Close-Grip Bench Press - 4 sets of 8-10 reps\n2. ..."
    exercises_reps = {}
    lines = day_info.split("\n")
    for line in lines:
        if line.strip().startswith("-"):
            continue
        if line.strip().startswith("Notes:"):
            break
        parts = line.split("-")
        if len(parts) > 1:
            exercise_name = parts[1].strip().split(" - ")[0].strip()
            sets_reps = parts[1].strip().split(" - ")[1].strip()
            exercises_reps[exercise_name] = sets_reps
    return exercises_reps

def register_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Exercise Database API! FElix is the best "

    @app.route('/list_of_body_parts', methods=['GET'])
    def list_of_body_parts():
        endpoint = f"{BASE_URL}/309/list+of+body+parts"
        data, status_code = fetch_api_data(endpoint)
        return jsonify(data), status_code

    @app.route('/list_exercise_by_body_part', methods=['GET'])
    def list_exercise_by_body_part():
        body_part = request.args.get('bodyPart', 'cardio')
        endpoint = f"{BASE_URL}/310/list+exercise+by+body+part"
        params = {'bodyPart': body_part}
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    @app.route('/list_by_target_muscle', methods=['GET'])
    def list_by_target_muscle():
        target = request.args.get('target', 'biceps')
        endpoint = f"{BASE_URL}/312/list+by+target+muscle"
        params = {'target': target}
        data, status_code = fetch_api_data(endpoint, params)
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
    
    @app.route('/create_schedule', methods=['POST'])
    def gather_info():
        try:
            data = request.get_json()
            if not data:
                logging.error("No data received")
                return jsonify({"status": "error", "message": "No data received"}), 400
            logger.debug("Received data: %s", data)

            
            age = int(data.get('age'))  # Ensure age is an integer
            gender = data.get('gender')
            weight = int(data.get('weight'))  # Ensure weight is an integer
            goal = data.get('goal')
            days = data.get('days')
            available_time_per_session = int(data.get('available_time'))  # Ensure available time is an integer
            
            logger.debug(f"Parsed data - age: {age}, gender: {gender}, weight: {weight}, goal: {goal}, days: {days}, available_time: {available_time_per_session}")

            gender = treat_gender_data(gender)
            logger.debug(f"Treated gender: {gender}")

            distributor = MuscleGroupDistributor(len(days))
            muscle_groups = distributor.distribute_muscle_groups()
            logger.debug(f"Treated muscles: {muscle_groups}")

             # Prepare data to send to external API
            api_data = {
                "gender": gender,
                "weight": weight,
                "goal": goal,
                "target_muscles": [muscle.value for muscle_group in muscle_groups for muscle in muscle_group]
            }

            logger.debug(f"API data: {api_data}")
            # Make API request
            api_response = call_external_api(api_data)
            logger.debug(f"API response: {api_response}")
            if api_response.get('status'):
                # Process API response to format into dictionary with days as keys
                routine = process_api_response(api_response)
                logger.debug(f"Routine: {routine}")

            
       

                # Use the custom JSON encoder to convert to a JSON string
                json_custom_schedule = json.dumps(routine, cls=CustomScheduleEncoder)
                app.logger.debug("JSON custom schedule: %s", json_custom_schedule)

                # Convert the JSON string back to a dictionary
                schedule_data = json.loads(json_custom_schedule)
                app.logger.debug("Schedule data (dictionary): %s", schedule_data)

                inserted_id = server_crud_operations(
                    operation="insert",
                    json_data={"schedule": schedule_data},
                    collection_name="schedules"
                )

                return jsonify({"status": "success", "routine": routine}), 200
            else:
                return jsonify({"status": "error", "message": "Failed to create routine"}), 500

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get-schedule/<schedule_id>', methods=['GET'])
    def get_schedule(schedule_id):
        try:
            # Convert the schedule_id to ObjectId
            schedule_id = ObjectId(schedule_id)
            
            # Read the schedule from the database
            schedule = server_crud_operations(
                operation="read",
                collection_name="schedules",
                key="_id",
                value=schedule_id
            )
            
            if schedule:
                return jsonify({"status": "success", "schedule": schedule}), 200
            else:
                return jsonify({"status": "error", "message": "Schedule not found"}), 404
        except Exception as e:
            print("Error:", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500
