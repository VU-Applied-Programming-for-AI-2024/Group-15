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

