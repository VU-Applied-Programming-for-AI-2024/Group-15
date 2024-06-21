from backend.app.models.day import Day
from backend.app.models.workout import Workout
from backend.app.models.workout_exercise import WorkoutExercise
from backend.app.models.exercise import Exercise
import re
import os
from utils.crud_operations_azure import create_collection_if_not_exists, read_document
import pymongo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CONNECTION_STRING = os.environ.get("MONGODB_STRING")
DB_NAME = "myFitnessAIcoach"
EXERCISE_COLLECTION = "exercises"

class Schedule:
    def __init__(self, routine):
        self.schedule = {day: None for day in Day}
        self._parse_routine(routine)

    def _parse_routine(self, routine):
        day_mapping = {
            "Day 1": Day.MONDAY,
            "Day 2": Day.TUESDAY,
            "Day 3": Day.WEDNESDAY,
            "Day 4": Day.THURSDAY,
            "Day 5": Day.FRIDAY,
            "Day 6": Day.SATURDAY,
            "Day 7": Day.SUNDAY
        }
        lines = routine[0].split('**')
        current_day = None
        workout = None

        exercise_pattern = re.compile(r'^(.*) - (\d+) sets? of (\d+)-(\d+) reps?$')

        for line in lines:
            line = line.strip()
            if line in day_mapping:
                if current_day and workout:
                    self.schedule[day_mapping[current_day]] = workout
                current_day = line
                workout = Workout()
            elif current_day and workout:
                exercises = line.split('\n')
                for exercise in exercises:
                    if exercise and not exercise.startswith('Day'):
                        match = exercise_pattern.match(exercise.strip())
                        if match:
                            name = match.group(1).strip()
                            sets = int(match.group(2))
                            reps = f"{match.group(3)}-{match.group(4)}"
                            # Creating a dummy Exercise instance
                            exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=name, target="unknown")
                            workout.add_exercise(WorkoutExercise(exercise_obj, sets, reps))
                        else:
                            # Creating a dummy Exercise instance for unmatched exercises
                            exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=exercise.strip(), target="unknown")
                            workout.add_exercise(WorkoutExercise(exercise_obj, 0, ""))
        if current_day and workout:
            self.schedule[day_mapping[current_day]] = workout

    def get_workout(self, day):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")
        return self.schedule.get(day)

    def generate_stats_for_day(self, day):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")

        workout = self.get_workout(day)
        if not workout:
            return {"error": f"No workout found for {day.name}"}

        # Fetch exercises from the database
        client = pymongo.MongoClient(CONNECTION_STRING)
        exercise_collection = create_collection_if_not_exists(client, EXERCISE_COLLECTION)

        exercises = []
        for workout_exercise in workout.exercises:
            exercise_data = exercise_collection.find_one({"name": workout_exercise.exercise.name})
            if exercise_data:
                exercise = Exercise(
                    body_part=exercise_data['body_part'],
                    equipment=exercise_data['equipment'],
                    gif_url=exercise_data['gif_url'],
                    exercise_id=exercise_data['exercise_id'],
                    name=exercise_data['name'],
                    target=exercise_data['target']
                )
                sets, reps = workout_exercise.sets, workout_exercise.reps
                workout_exercise = WorkoutExercise(
                    exercise=exercise,
                    sets=sets,
                    reps=reps
                )
                exercises.append(workout_exercise)

        return self.calculate_statistics(exercises)

    def calculate_statistics(self, exercises):
        intensity = [40, 35, 25]  # Example static values, you can compute based on exercises
        calories_burned = sum(exercise.sets * int(exercise.reps.split('-')[1]) * 0.5 for exercise in exercises)  # Example calculation
        targeted_muscles = list(set(exercise.exercise.target for exercise in exercises))
        sets_per_muscle_group = {exercise.exercise.target: exercise.sets for exercise in exercises}

        stats = {
            "intensity": intensity,
            "calories_burned": calories_burned,
            "targeted_muscles": targeted_muscles,
            "sets_per_muscle_group": sets_per_muscle_group
        }
        return stats

    def __repr__(self):
        return f"Schedule(schedule={self.schedule})"
