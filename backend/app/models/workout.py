from backend.app.models.workout_exercise import WorkoutExercise

class Workout:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, workout_exercise):
        if isinstance(workout_exercise, WorkoutExercise):
            self.exercises.append(workout_exercise)
        else:
            raise ValueError("Only instances of WorkoutExercise can be added")

    def calculate_workout_time(self):
        total_time = 0  # in seconds
        walking_time = 5 * 60  # 5 minutes walking time between exercises

        for i, workout_exercise in enumerate(self.exercises):
            reps_time = workout_exercise.sets * workout_exercise.reps * 3  # each rep takes 3 seconds
            rest_time = (workout_exercise.sets - 1) * 60  # 1 minute rest between sets

            total_time += reps_time + rest_time

            if i < len(self.exercises) - 1:  # Add walking time except for the last exercise
                total_time += walking_time

        # Convert total_time to minutes and seconds
        minutes, seconds = divmod(total_time, 60)
        return f"{minutes} minutes and {seconds} seconds"

    def __repr__(self):
        return f"Workout(exercises={self.exercises})"



