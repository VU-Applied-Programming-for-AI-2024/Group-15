from flask import jsonify, request
import requests
import os 
from typing import List, Any, Union
from dotenv import load_dotenv, find_dotenv
from models.day import Day
from models.bodypart import BodyPart
from models.schedule import Schedule
from models.exercise import Exercise, WorkoutExercise
from models.workout import Workout
import re

load_dotenv(find_dotenv())

API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_KEY = os.environ.get("EXERCISE_API_KEY")
BASE_URL = os.environ.get("API_ENDPOINT")

def fetch_api_data(endpoint, params=None):
    """Fetch data from the external API."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch data from the API"}, response.status_code

def register_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Exercise Database API!"

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

    @app.route('/list_by_equipment', methods=['GET'])
    def list_by_equipment():
        equipment = request.args.get('equipment', 'medicine ball')
        endpoint = f"{BASE_URL}/2083/list+by+equipment"
        params = {'equipment': equipment}
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    @app.route('/ai_workout_planner', methods=['GET'])
    def ai_workout_planner():
        target = request.args.get('target', 'triceps')
        gender = request.args.get('gender', 'male')
        weight = request.args.get('weight', '80')
        goal = request.args.get('goal', 'muscle_gain')
        endpoint = f"{BASE_URL}/4824/ai+workout+planner"
        params = {
            'target': target,
            'gender': gender,
            'weight': weight,
            'goal': goal
        }
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    @app.route('/calories_burned', methods=['GET'])
    def calories_burned():
        age = request.args.get('age', '24')
        gender = request.args.get('gender', 'male')
        weight = request.args.get('weight', '80')
        exercise_id = request.args.get('exercise_id', '745')
        reps = request.args.get('reps', '25')
        lifted_weight = request.args.get('lifted_weight', None)
        minutes = request.args.get('minutes', None)
        endpoint = f"{BASE_URL}/4825/calories+burned"
        params = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'exercise_id': exercise_id,
            'reps': reps,
            'lifted_weight': lifted_weight,
            'minutes': minutes
        }
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    def search_exercises(user_input, bodypart, equipment):
        """
        Search for exercises based on user input, body part, and equipment.
        
        Parameters:
        - user_input (str): The search string provided by the user.
        - bodypart (str): The body part to filter exercises.
        - equipment (str): The equipment to filter exercises.
        
        Returns:
        - list: A list of exercises matching the search criteria.
        """
        # Fetch exercises for the specified body part
        endpoint = f"{BASE_URL}/310/list+exercise+by+body+part"
        params = {'bodyPart': bodypart}
        exercises, status_code = fetch_api_data(endpoint, params)
        
        if status_code != 200:
            return {"error": "Failed to fetch exercises"}, status_code

        # Filter exercises based on user input and equipment
        filtered_exercises = [
            exercise for exercise in exercises
            if (user_input.lower() in exercise['name'].lower() or 
                user_input.lower() in exercise['description'].lower()) and 
            (equipment.lower() in exercise['equipment'].lower())
        ]

        return filtered_exercises, 200

    @app.route('/search_exercises', methods=['GET'])
    def search_exercises_route():
        user_input = request.args.get('user_input', '')
        bodypart = request.args.get('bodypart', '')
        equipment = request.args.get('equipment', '')

        exercises, status_code = search_exercises(user_input, bodypart, equipment)
        return jsonify(exercises), status_code
    
    def create_custom_schedule(gender, weight, goal, bodyparts, days):
        routines = []

        for bodypart in bodyparts:
            for target_muscle in bodypart.value:
                endpoint = f"{BASE_URL}/4824/ai+workout+planner"
                params = {
                    'target': target_muscle,
                    'gender': gender,
                    'weight': weight,
                    'goal': goal
                }
                data, status_code = fetch_api_data(endpoint, params)
                if status_code == 200 and 'routine' in data:
                    routines.append(data['routine'][0])

        custom_schedule = {day: Workout() for day in days}
        day_index = 0

        exercise_pattern = re.compile(r'^(.*) - (\d+) sets? of (\d+)-(\d+) reps?$')

        for routine in routines:
            lines = routine.split('**')
            current_workout = None

            for line in lines:
                line = line.strip()
                if 'Day' in line:
                    if current_workout:
                        custom_schedule[days[day_index % len(days)]] = current_workout
                        day_index += 1
                    current_workout = Workout()
                elif current_workout:
                    exercises = line.split('\n')
                    for exercise in exercises:
                        if exercise and not exercise.startswith('Day'):
                            match = exercise_pattern.match(exercise.strip())
                            if match:
                                name = match.group(1).strip()
                                sets = int(match.group(2))
                                reps = f"{match.group(3)}-{match.group(4)}"
                                exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=name, target="unknown")
                                current_workout.add_exercise(WorkoutExercise(exercise_obj, sets, reps))
                            else:
                                exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=exercise.strip(), target="unknown")
                                current_workout.add_exercise(WorkoutExercise(exercise_obj, 0, ""))
            if current_workout:
                custom_schedule[days[day_index % len(days)]] = current_workout
                day_index += 1

        return Schedule([str(custom_schedule[day]) for day in days])