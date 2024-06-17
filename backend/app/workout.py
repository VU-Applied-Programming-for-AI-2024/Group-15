from backend.app.workout_exercise import ExerciseDetail

from workout_exercise import WorkoutExercise

class Workout:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, workout_exercise):
        if isinstance(workout_exercise, WorkoutExercise):
            self.exercises.append(workout_exercise)
        else:
            raise ValueError("Only instances of WorkoutExercise can be added")

    def __repr__(self):
        return f"Workout(exercises={self.exercises})"


