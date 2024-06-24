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

load_dotenv(find_dotenv())


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
    def gather_info():
        try:
            data = request.get_json()
            
            
            age = int(data.get('age'))
            gender = data.get('gender')
            weight = int(data.get('weight')) 
            goal = data.get('goal')
            days = data.get('days')
            available_time_per_session = int(data.get('available_time')) 

            gender = treat_gender_data(gender)

            custom_schedule = create_custom_schedule(gender, weight, goal, days, available_time_per_session)
            json_custom_schedule = json.dumps(custom_schedule, cls=CustomScheduleEncoder)
            schedule_data = json.loads(json_custom_schedule)

            inserted_id = server_crud_operations(
                operation="insert",
                json_data={"schedule": schedule_data},
                collection_name="schedules"
            )

            return jsonify({"status": "success", "message": "Schedule created successfully", "schedule_id": str(inserted_id)}), 200
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

def fetch_api_data_async(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from the API!"}

def create_custom_schedule(gender: str, weight: int, goal: str, days: List[str], available_time_per_session: int):
    distributor = MuscleGroupDistributor(len(days))
    muscle_groups_schedule = distributor.distribute_muscle_groups()

    api_calls = []
    for i, day_muscles in enumerate(muscle_groups_schedule):
        for muscle in day_muscles:
            for target in muscle.value:
                api_calls.append((days[i], f"{BASE_URL}/4824/ai+workout+planner", {'target': target, 'gender': gender, 'weight': weight, 'goal': goal}))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_params = {executor.submit(fetch_api_data_async, endpoint, params): (day, params['target']) for day, endpoint, params in api_calls}
        api_results = {(day, target): future.result() for future, (day, target) in future_to_params.items()}

    # Organize routines by day
    routines = {day: [] for day in days}
    for (day, target), result in api_results.items():
        if 'routine' in result:
            routines[day].append(result['routine'][0])

    custom_schedule = {day: Workout() for day in days}
    exercise_pattern = re.compile(r'^(.*) - (\d+) sets? of (\d+)-(\d+) reps?$')
    print(exercise_pattern)
    for day, daily_routines in routines.items():
        current_workout = Workout()
        for routine in daily_routines:
            lines = routine.split('**')
            for line in lines:
                line = line.strip()
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
            
            total_time, _ = current_workout.calculate_workout_time()
            if total_time > available_time_per_session:
                break

        custom_schedule[day] = current_workout

    return Schedule([custom_schedule[day] for day in days])