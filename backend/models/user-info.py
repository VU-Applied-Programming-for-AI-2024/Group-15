from flask import Flask, jsonify, request,Response, redirect, url_for, render_template
import os
import requests
from flask_cors import CORS
import re
from typing import Union, Tuple, Optional, List
from routes import create_custom_schedule
from models.bodypart import BodyPart
from pymongo import MongoClient
import pymongo.errors
from utils.crud_operations_azure import server_crud_operations

app = Flask(__name__)
CORS(app)

@app.route('/api/create-schedule', methods=['POST'])
def gather_info():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Extracting individual fields for debugging
        age = data.get('age')
        gender = data.get('gender')
        weight = data.get('weight')
        muscles = data.get('muscles')
        goal = data.get('goal')
        days = data.get('days')

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
            # Ensure that the API isn't confused about gender   
            if gender == "other":
                gender = "female"

        custom_schedule = create_custom_schedule(gender, weight, goal, muscle_list, days)
        
        # Insert the custom schedule into MongoDB
        server_crud_operations(
            operation="insert",
            json_data={"schedule": custom_schedule},
            collection_name="schedules"
        )
        
        # Return a success response
        return jsonify({"status": "success", "message": "Schedule created successfully", "schedule": custom_schedule}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
