from models.exercise import Exercise

class WorkoutExercise:
    def __init__(self, exercise, sets, reps):
        if isinstance(exercise, Exercise):
            self.exercise = exercise
        else:
            raise ValueError("Exercise must be an instance of the Exercise class")
        self.sets = sets
        self.reps = reps

    def __repr__(self):
        return f"WorkoutExercise(exercise={self.exercise}, sets={self.sets}, reps={self.reps})"
