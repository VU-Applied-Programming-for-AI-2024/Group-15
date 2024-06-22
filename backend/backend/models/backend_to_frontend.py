from flask import Flask, jsonify
import pymongo
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
load_dotenv()

CONNECTION_STRING = os.environ.get("MONGODB_STRING")
client = pymongo.MongoClient(CONNECTION_STRING)
DB_NAME = "myFitnessAIcoach"
collection_name = "workouts"

@app.route('/api/schedule', methods=['GET'])
def get_the_schedule():
    collection = client[DB_NAME][collection_name]
    schedule = list(collection.find({}, {'_id': False}))  # Retrieve all data and exclude the MongoDB _id field
    return jsonify(schedule)


# Mock data that simulates the structure of your actual MongoDB data

mock_data = [
    {
        "day": "Monday",
        "exercises": [
            {"name": "Push Up", "sets": 3, "reps": 10},
            {"name": "Squat", "sets": 3, "reps": 15}
        ]
    },
    {
        "day": "Wednesday",
        "exercises": [
            {"name": "Pull Up", "sets": 3, "reps": 8},
            {"name": "Lunge", "sets": 3, "reps": 12}
        ]
    },
    {
        "day": "Friday",
        "exercises": [
            {"name": "Bench Press", "sets": 3, "reps": 10},
            {"name": "Deadlift", "sets": 3, "reps": 12}
        ]
    }
]

@app.route('/mock_schedule', methods=['GET'])
def mock_schedule():
    return jsonify(mock_data)

if __name__ == '__main__':
    app.run(debug=True)