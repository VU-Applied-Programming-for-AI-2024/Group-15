from flask import Flask, jsonify, request,Response, redirect, url_for, render_template
import os
import requests
from flask_cors import CORS
import re
from app import app 
from typing import Union, Tuple, Optional, List
from routes import create_custom_schedule
from models.bodypart import BodyPart
from pymongo import MongoClient
import pymongo.errors
from utils.crud_operations_azure import server_crud_operations
from models.exercise import Exercise
from models.workout_exercise import WorkoutExercise
from models.workout import Workout
from models.schedule import Schedule
import json
from bson import ObjectId

#This class helps handling the data from the custom_schedule
class CustomScheduleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BodyPart):
            return obj.value
        elif isinstance(obj, Exercise):
            return obj.name
        elif isinstance(obj, WorkoutExercise):
            return {
                'exercise': obj.exercise.name,
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

def treat_gender_data (gender)->str:
    # Ensure that the API isn't confused about gender   
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


@app.route('/api/create-schedule', methods=['POST'])
def gather_info():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        age = data.get('age')
        gender = data.get('gender')
        weight = data.get('weight')
        goal = data.get('goal')
        days = data.get('days')
        available_time_per_session = int(data.get('available_time'))

        gender = treat_gender_data(gender)

        custom_schedule = create_custom_schedule(gender, weight, goal, days, available_time_per_session)

        json_custom_schedule = json.dumps(custom_schedule, cls=CustomScheduleEncoder)

        inserted_id = server_crud_operations(
            operation="insert",
            json_data={"schedule": json_custom_schedule},
            collection_name="chedules"
        )
        
        return jsonify({"status": "success", "message": "Schedule created successfully", "schedule_id": str(inserted_id)}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/api/get-schedule/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    try:
        # Convert the schedule_id to ObjectId
        schedule_id = ObjectId(schedule_id)
        
        # Read the schedule from the database
        schedule = server_crud_operations(
            operation="read",
            collection_name="Schedules",
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