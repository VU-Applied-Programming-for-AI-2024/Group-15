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
import openai
import logging 

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_KEY = os.environ.get("EXERCISE_API_KEY")
BASE_URL = os.environ.get("API_ENDPOINT")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
openai.api_key = os.getenv("OPENAI_KEY")

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

def parse_exercise_response(response_text):
    try:
        prompt = f"""
        Extract the exercises from the following response and provide them in a structured JSON format, but remember you don't have to cpy the input or leave comments or anything else, I just want the pure json file from you, with only the name of the exercise, the sets and the number of reps per each set. In this format: 
        

        {response_text}

        The format should be:
        {{
          "Day 1": [
            {{
              "exercise": "exercise_name",
              "sets": x,
              "reps": y,
            }},
            ...
          ]
        }}

        Please only return the JSON data without any additional text or formatting. Here is the provided data:
        {response_text}
        """
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extracting the response content
        structured_data = completion.choices[0].message['content'].strip()
        logger.info(f"Structured data from OpenAI: {structured_data}")

        # Ensure the response is a valid JSON
        try:
            # Only take the part inside the JSON block
            start_idx = structured_data.find('{')
            end_idx = structured_data.rfind('}') + 1
            json_str = structured_data[start_idx:end_idx]
            return json.loads(json_str)
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decode error: {json_err}")
            raise ValueError("Invalid JSON response from OpenAI")
        
    except Exception as e:
        logger.error(f"Error in parsing exercise response: {str(e)}")
        logger.error(f"Response from OpenAI: {response_text}")
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

            gender = "female" if gender == "other" else gender

            custom_schedule = create_custom_schedule(gender, weight, goal, days, available_time_per_session)
            structured_workout = structure_workout_by_time(custom_schedule, len(days), available_time_per_session)
            
            return jsonify(structured_workout), 200
        except Exception as e:
            app.logger.error("Error: %s", str(e))
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
        
    @app.route('/store-schedule', methods=['POST'])
    def store_schedule():
        try:
            schedule = request.get_json()
            
            inserted_id = server_crud_operations(
                operation="insert",
                json_data={"schedule": schedule},
                collection_name="schedules"
            )

            return jsonify({"status": "success", "message": "Schedule stored successfully", "schedule_id": str(inserted_id)}), 200
        except Exception as e:
            app.logger.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

def fetch_api_data_async(endpoint, params):
    headers = {'Authorization': 'Bearer 4623|B0oWv01vaf4fCpyzvGYwrHiWQI1Jh1fy60FbgBrh'}
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()

def create_custom_schedule(gender, weight, goal, days, available_time_per_session):
    distributor = MuscleGroupDistributor(len(days))
    muscle_groups_schedule = distributor.distribute_muscle_groups()

    api_calls = []
    for day_muscles in muscle_groups_schedule:
        for muscle in day_muscles:
            for target in muscle.value:
                api_calls.append((f"{BASE_URL}/4824/ai+workout+planner", {'target': target, 'gender': gender, 'weight': weight, 'goal': goal}))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_params = {executor.submit(fetch_api_data_async, endpoint, params): (endpoint, params) for endpoint, params in api_calls}
        api_results = [future.result() for future in future_to_params]

    workout_data = {}
    for i, api_response in enumerate(api_results):
        try:
            day = f"Day {i + 1}"
            logger.info(f"API response for {day}: {api_response}")
            workout_data[day] = parse_exercise_response(api_response['routine'][0])
        except Exception as e:
            logger.error(f"Error processing day {i + 1}: {e}")
            continue

    return workout_data

def structure_workout_by_time(all_exercises, days, available_time_per_session):
    workout_schedule = {f"Day {i+1}": [] for i in range(days)}
    current_day = 1
    workout = Workout()

    for day, exercises in all_exercises.items():
        for exercise in exercises:
            workout_exercise = WorkoutExercise(
                exercise=Exercise(
                    body_part=exercise['bodyPart'],
                    equipment=exercise['equipment'],
                    gif_url=exercise['gifUrl'],
                    exercise_id=exercise['id'],
                    name=exercise['name'],
                    target=exercise['target'],
                ),
                sets=exercise['sets'],
                reps=exercise['reps'],
            )
            
            workout.add_exercise(workout_exercise)
            total_time, _ = workout.calculate_workout_time()
            
            if total_time > available_time_per_session * 60:
                current_day += 1
                if current_day > days:
                    break
                workout = Workout()
                workout.add_exercise(workout_exercise)
            
            workout_schedule[f"Day {current_day}"].append({
                'exercise': exercise['name'],
                'sets': exercise['sets'],
                'reps': exercise['reps'],
            })

    return workout_schedule
