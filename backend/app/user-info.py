from flask import Flask, jsonify, request,Response, redirect, url_for, render_template
import os
import requests
from flask_cors import CORS
import re
from typing import Union, Tuple, Optional, List


@app.route('/api/create-schedule', methods=['POST'])
def create_schedule():
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
        
        print("Age:", age)
        print("Gender:", gender)
        print("Weight:", weight)
        print("Muscles:", muscles)
        print("Goal:", goal)
        print("Days:", days)
        
        # Here you can add your logic to process the data and create a schedule
        
        # Return a success response
        return jsonify({"status": "success", "message": "Schedule created successfully"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
