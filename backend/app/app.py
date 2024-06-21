from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from bson import ObjectId 
from models.bodypart import BodyPart
from routes import register_routes, create_custom_schedule
from utils.crud_operations_azure import server_crud_operations, retrieve_all_values_for_key, create_collection_if_not_exists
from utils.crud_operations_azure import insert_document, find_all_documents

def create_app():
    app = Flask(__name__)
    CORS(app)

    logging.basicConfig(level=logging.INFO)
    register_routes(app)

    load_dotenv(find_dotenv())
    CONNECTION_STRING = os.getenv("MONGODB_STRING")
    DB_NAME = "myFitnessAIcoach"

    # Connect to MongoDB
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]

    @app.route('/api/create-schedule', methods=['POST'])
    def create_schedule():
        try:
            data = request.get_json()
            logging.info("Received data: %s", data)

            # Extract data from request JSON
            age = data.get('age')
            gender = data.get('gender')
            weight = data.get('weight')
            muscles = data.get('muscles')
            goal = data.get('goal')
            days = data.get('days')
            

            # # Map muscle names to BodyPart enum values
            muscle_list = []
            for muscle_name in muscles:
                for part in BodyPart:
                    if muscle_name.lower() in [m.lower() for m in part.value]:
                        muscle_list.append(part)
                        break
                else:
                    raise ValueError(f"Muscle '{muscle_name}' not found in BodyPart enum")

            # Call create_custom_schedule function
            custom_schedule = create_custom_schedule(gender, weight, goal, muscle_list, days)

            # Prepare data for MongoDB insertion
            schedule_data = {
                "schedule": custom_schedule,
                "age": age,
                "gender": gender,
                "weight": weight,
                "goal": goal,
                "days": days,
                "muscles": muscles
            }

            # Insert schedule data into MongoDB
            collection_name = "schedules"
            collection = create_collection_if_not_exists(client, collection_name)
            schedule_id = insert_document(collection, schedule_data)

            return jsonify({
                "status": "success",
                "message": "Schedule created successfully",
                "schedule_id": str(schedule_id)
            }), 200

        except Exception as e:
            logging.error("Error: %s", str(e))
            return jsonify({"status": "error", f"message is ": str(e)}), 500

    @app.route('/api/schedules', methods=['GET'])
    def get_all_schedules():
        try:
            # Retrieve all schedules from MongoDB
            collection_name = "schedules"
            collection = create_collection_if_not_exists(client, collection_name)
            schedules = find_all_documents(collection)

            return jsonify({"status": "success", "schedules": schedules}), 200

        except Exception as e:
            logging.error("Error: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

    return app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
