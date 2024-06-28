from flask import jsonify, request, Flask
import requests
import os
from typing import List, Any, Union, Dict, Tuple
from dotenv import load_dotenv, find_dotenv
from utils.crud_operations_azure import server_crud_operations
import json
import openai
import logging
import uuid

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_KEY: str = os.environ.get("OPENAI_KEY")
openai.api_key = os.getenv("OPENAI_KEY")
API_ENDPOINT: str = os.environ.get("API_ENDPOINT")
API_KEY: str = os.environ.get("EXERCISE_API_KEY")
BASE_URL: str = os.environ.get("API_ENDPOINT")
OPENAI_KEY = os.environ.get("OPENAI_KEY")


def create_schedule_with_openai(age: int, gender: str, weight: int, goal: str, days: List[str], available_time: int) -> Dict[str, Any]:
    """
    Creates a workout schedule using OpenAI's API.

    Args:
        age (int): Age of the user.
        gender (str): Gender of the user.
        weight (int): Weight of the user in kg.
        goal (str): Fitness goal of the user.
        days (List[str]): Days of the week the user plans to workout.
        available_time (int): Available time per session in minutes.

    Returns:
        Dict[str, Any]: The workout schedule in JSON format.
    """
    try:
        prompt: str = f"""
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

        response: openai.Completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        structured_data: str = response.choices[0].message['content'].strip()
        logger.info(f"Structured data from OpenAI: {structured_data}")

        json_data: Dict[str, Any] = json.loads(structured_data)
        return json_data

    except json.JSONDecodeError as json_err:
        logger.error(f"JSON decode error: {json_err}")
        raise ValueError("Invalid JSON response from OpenAI")
    except Exception as e:
        logger.error(f"Error in parsing exercise response: {str(e)}")
        raise

def search_exercises(user_input: str, bodypart: str, equipment: str) -> Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]:
    """
    Searches for exercises based on user input, body part, and equipment.

    Args:
        user_input (str): User input to search exercises.
        bodypart (str): Body part to filter exercises.
        equipment (str): Equipment to filter exercises.

    Returns:
        Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]: Filtered exercises and the status code.
    """
    endpoint: str = f"{BASE_URL}/310/list+exercise+by+body+part"
    params: Dict[str, str] = {'bodyPart': bodypart}
    exercises, status_code = fetch_api_data(endpoint, params)
    
    if status_code != 200:
        return {"error": "Failed to fetch exercises"}, status_code

    filtered_exercises: List[Dict[str, Any]] = [
        exercise for exercise in exercises
        if (user_input.lower() in exercise['name'].lower() or 
            user_input.lower() in exercise['target'].lower()) and 
        (equipment.lower() in exercise['equipment'].lower())
    ]

    return filtered_exercises, 200

def fetch_api_data(endpoint: str, params: Dict[str, str] = None) -> Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]:
    """
    Fetches data from the API.

    Args:
        endpoint (str): API endpoint to fetch data from.
        params (Dict[str, str], optional): Parameters to pass with the API request. Defaults to None.

    Returns:
        Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]: The data fetched from the API and the status code.
    """
    headers: Dict[str, str] = {"Authorization": f"Bearer {API_KEY}"}
    response: requests.Response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch data from the API!"}, response.status_code

def register_routes(app: Flask) -> None:
    """
    Registers all routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.route('/')
    def home() -> str:
        """
        Home route.

        Returns:
            str: Welcome message.
        """
        return "Welcome to the Exercise Database API! FElix is the best "

    @app.route('/list_of_body_parts', methods=['GET'])
    def list_of_body_parts() -> Tuple[Union[Dict[str, str], List[str]], int]:
        """
        Route to list all body parts.

        Returns:
            Tuple[Union[Dict[str, str], List[str]], int]: List of body parts and the status code.
        """
        endpoint: str = f"{BASE_URL}/309/list+of+body+parts"
        data, status_code = fetch_api_data(endpoint)
        return jsonify(data), status_code

    @app.route('/exercise_by_id', methods=['GET'])
    def exercise_by_id() -> Tuple[Union[Dict[str, str], Dict[str, Any]], int]:
        """
        Route to get exercise by ID.

        Returns:
            Tuple[Union[Dict[str, str], Dict[str, Any]], int]: Exercise details and the status code.
        """
        exercise_id: str = request.args.get('id', '14')
        endpoint: str = f"{BASE_URL}/1004/exercise+by+id"
        params: Dict[str, str] = {'id': exercise_id}
        data, status_code = fetch_api_data(endpoint, params)
        return jsonify(data), status_code

    @app.route('/list_of_equipment', methods=['GET'])
    def list_of_equipment() -> Tuple[Union[Dict[str, str], List[str]], int]:
        """
        Route to list all equipment.

        Returns:
            Tuple[Union[Dict[str, str], List[str]], int]: List of equipment and the status code.
        """
        endpoint: str = f"{BASE_URL}/2082/list+of+equipment"
        data, status_code = fetch_api_data(endpoint)
        return jsonify(data), status_code

    @app.route('/search_exercises', methods=['GET'])
    def search_exercises_route() -> Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]:
        """
        Route to search for exercises based on user input, body part, and equipment.

        Returns:
            Tuple[Union[Dict[str, str], List[Dict[str, Any]]], int]: Filtered exercises and the status code.
        """
        user_input: str = request.args.get('user_input', '')
        bodypart: str = request.args.get('bodypart', '')
        equipment: str = request.args.get('equipment', '')

        exercises, status_code = search_exercises(user_input, bodypart, equipment)
        return jsonify(exercises), status_code
    
    @app.route('/get_favorites', methods=['GET'])
    def get_favorites_by_email() -> Tuple[Dict[str, Any], int]:
        """
        Route to get favorite exercises by email.

        Returns:
            Tuple[Dict[str, Any], int]: Favorite exercises and the status code.
        """
        try:
            email: str = request.args.get('email')
            
            if not email:
                return jsonify({"status": "error", "message": "Email parameter is required"}), 400
            
            favorites: List[Dict[str, Any]] = server_crud_operations(
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
    def add_to_favorites() -> Tuple[Dict[str, Any], int]:
        """
        Route to add a workout schedule to favorites.

        Returns:
            Tuple[Dict[str, Any], int]: Success or error message and the status code.
        """
        try:
            data: Dict[str, Any] = request.json
            if not data:
                raise ValueError("No JSON data provided")

            email: str = data.get('email')
            schedule_name: str = data.get('scheduleName')
            schedule: Dict[str, Any] = data.get('schedule')

            if not email or not schedule_name or not schedule:
                raise ValueError("Missing required fields: email, scheduleName, or schedule")

            # Create the favorite document
            favorite: Dict[str, Any] = {
                "_id": email + schedule_name,
                "email": email,
                "schedule_name": schedule_name,
                "schedule": schedule
            }

            # Log the favorite document for debugging
            logger.debug(f"Favorite document: {favorite}")

            # Perform the database operation
            server_crud_operations(
                operation="insert",
                json_data={"favorite": favorite},
                collection_name="favorites"
            )

            # Return success response
            return jsonify({"status": "success", "message": "Schedule added to favorites successfully"}), 200

        except ValueError as ve:
            logger.error(f"Validation Error: {str(ve)}")
            return jsonify({"status": "error", "message": str(ve)}), 400

        except Exception as e:
            logger.error(f"Error adding schedule to favorites: {str(e)}")
            return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    
    @app.route('/create-schedule', methods=['POST'])
    def create_schedule() -> Tuple[Dict[str, Any], int]:
        """
        Route to create a workout schedule.

        Returns:
            Tuple[Dict[str, Any], int]: The created schedule and the status code.
        """
        try:
            data: Dict[str, Any] = request.get_json()
            app.logger.info(f"Received data: {data}")
            
            age: int = int(data.get('age'))
            gender: str = data.get('gender')
            weight: int = int(data.get('weight'))
            goal: str = data.get('goal')
            days: List[str] = data.get('days')
            available_time_per_session: int = int(data.get('available_time'))

            schedule: Dict[str, Any] = create_schedule_with_openai(age, gender, weight, goal, days, available_time_per_session)

            # Generate unique string ID for the schedule
            schedule_id: str = str(uuid.uuid4())
            schedule["_id"] = schedule_id

            # Store the schedule in the database
            inserted_id: str = server_crud_operations(
                operation="insert",
                json_data=schedule,
                collection_name="Schedules"
            )

            return jsonify({"status": "success", "schedule_id": schedule_id, "schedule": schedule}), 200
        except Exception as e:
            app.logger.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get-schedule/<schedule_id>', methods=['GET'])
    def get_schedule(schedule_id: str) -> Tuple[Dict[str, Any], int]:
        """
        Route to get a workout schedule by ID.

        Args:
            schedule_id (str): The ID of the schedule to retrieve.

        Returns:
            Tuple[Dict[str, Any], int]: The retrieved schedule and the status code.
        """
        try:
            logger.info(f"Received request to get schedule with id: {schedule_id}")
            result: Dict[str, Any] = server_crud_operations(
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
