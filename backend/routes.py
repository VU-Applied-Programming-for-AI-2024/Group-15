from flask import jsonify, request
import requests
import os
from requests.adapters import HTTPAdapter

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
from models.bodypart import MuscleGroupDistributor, BodyPart
from urllib3.util.retry import Retry
import concurrent.futures
import random
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
            return obj.value  
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
    
  
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
  
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(endpoint, headers=headers, params=params, verify=False)  # Set verify=False temporarily
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {"error": "Failed to fetch data from the API!"}, response.status_code
    except requests.exceptions.SSLError as ssl_error:
        return {"error": f"SSL Error: {str(ssl_error)}"}, 500
    except requests.exceptions.RequestException as req_error:
        return {"error": f"Request Error: {str(req_error)}"}, 500

def register_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Exercise Database API! Felix is the best"

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
    
    @app.route('/create-schedule', methods=['POST'])
    def gather_info():
        try:
            data = request.get_json()
            if not data:
                raise ValueError("No JSON data received")
            

            age = int(data.get('age'))
            gender = data.get('gender')
            
            weight = int(data.get('weight')) 
            goal = data.get('goal')
            days = data.get('days')
            available_time_per_session = int(data.get('available_time')) 


            print(f"Received data for creating schedule: %s,gender: {gender}, {weight}, {goal}, {days}, {available_time_per_session}")
            gender = treat_gender_data(gender)

             
            

            custom_schedule = create_custom_schedule(gender, weight, goal, days, available_time_per_session)
            json_custom_schedule = json.dumps(custom_schedule, cls=CustomScheduleEncoder)
            logger.info('Creating custom schedule...')
            schedule_data = json.loads(json_custom_schedule)

            inserted_id = server_crud_operations(
                operation="insert",
                json_data={"schedule": schedule_data},
                collection_name="schedules"
            )
            logger.info('Custom schedule created successfully')
            return jsonify({"status": "success", "message": "Schedule created successfully", "schedule_id": str(inserted_id)}), 200
        except Exception as e:
            logger.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get-schedule/<schedule_id>', methods=['GET'])
    def get_schedule(schedule_id):
        try:
            schedule_id = ObjectId(schedule_id)
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

def fetch_api_data_async(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the API!"}

import logging



def create_custom_schedule(gender: str, weight: int, goal: str, days: List[str], available_time_per_session: int):
    distributor = MuscleGroupDistributor(len(days))
    muscle_groups_schedule = distributor.distribute_muscle_groups()

    custom_schedule = {day: Workout() for day in days}

    for i, day_muscles in enumerate(muscle_groups_schedule):
        current_workout = Workout()
        day_enum = days[i].upper()  

        #
        random_body_part = random.choice(day_muscles)
        muscles = distributor.get_specific_muscles(random_body_part)  

        for muscle in muscles:
            exercise_added = False
            tries = 0
            exercises = []
            status_code = 500

            logger.info(f"Fetching exercises for muscle: {muscle}")

          
            while not exercise_added and tries < 10:
                try:
                    exercises, status_code = search_exercises(user_input='', bodypart=muscle, equipment='') 
                except Exception as e:
                    logger.error(f"Error fetching exercises: {e}")

                logger.info(f"Fetched {len(exercises)} exercises with status code {status_code}")

                if status_code == 200 and exercises:
                    try:
                        exercise_data = random.choice(exercises)
                        exercise_obj = Exercise(
                            body_part=random_body_part,  
                            equipment=exercise_data['equipment'],
                            gif_url=exercise_data['gifUrl'],
                            exercise_id=exercise_data['id'],
                            name=exercise_data['name'],
                            target=exercise_data['target']
                        )
                        workout_exercise = WorkoutExercise(exercise=exercise_obj, sets=3, reps="8-12")
                        current_workout.add_exercise(workout_exercise)
                        exercise_added = True
                    except Exception as e:
                        logger.error(f"Error adding exercise: {e}")
                tries += 1

            # If no exercise was added after 10 tries, fallback to the quickest exercise
            if not exercise_added and exercises:
                try:
                    quickest_exercise = min(exercises, key=lambda ex: ex['duration'])
                    exercise_obj = Exercise(
                        body_part=random_body_part,  # Use random_body_part as string
                        equipment=quickest_exercise['equipment'],
                        gif_url=quickest_exercise['gifUrl'],
                        exercise_id=quickest_exercise['id'],
                        name=quickest_exercise['name'],
                        target=quickest_exercise['target']
                    )
                    workout_exercise = WorkoutExercise(exercise=exercise_obj, sets=3, reps="8-12")
                    current_workout.add_exercise(workout_exercise)
                except Exception as e:
                    logger.error(f"Error adding fallback exercise: {e}")

        # Check if the workout exceeds available time per session
        total_time, _ = current_workout.calculate_workout_time()
        if total_time <= available_time_per_session:
            custom_schedule[day_enum] = current_workout
        else:
            # Handle the case where the workout exceeds available time
            while total_time > available_time_per_session and current_workout.exercises:
                current_workout.exercises.pop()
                total_time, _ = current_workout.calculate_workout_time()
            custom_schedule[day_enum] = current_workout


    schedule_input = {day: custom_schedule[day] for day in custom_schedule.keys()}

    return Schedule([schedule_input[day] for day in custom_schedule.keys()])