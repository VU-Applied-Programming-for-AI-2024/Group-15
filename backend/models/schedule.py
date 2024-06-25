from models.day import Day
from models.exercise import Exercise
from models.workout_exercise import WorkoutExercise
from models.workout import Workout
from typing import Dict, Any
import re 


class Schedule:
    def __init__(self, routine: Dict[str, Any]):
        self.schedule = {day: None for day in Day}
        self._parse_routine(routine)

    def _parse_routine(self, routine: Dict[str, Any]):
        for day_name, workout_data in routine.items():
            day_enum = Day[day_name.upper()]
            workout = Workout()
            for exercise_data in workout_data['exercises']:
                exercise_obj = Exercise(
                    body_part=exercise_data['bodyPart'],
                    equipment=exercise_data['equipment'],
                    gif_url=exercise_data['gifUrl'],
                    exercise_id=exercise_data['id'],
                    name=exercise_data['name'],
                    target=exercise_data['target']
                )
                workout_exercise = WorkoutExercise(
                    exercise=exercise_obj,
                    sets=exercise_data.get('sets', 3),  # Default to 3 sets if not provided
                    reps=exercise_data.get('reps', "8-12")  # Default to 8-12 reps if not provided
                )
                workout.add_exercise(workout_exercise)
            self.schedule[day_enum] = workout

    def get_workout(self, day: Day):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")
        return self.schedule.get(day)

    def __repr__(self):
        return f"Schedule(schedule={self.schedule})"
