from exercise import Exercise

class Workout:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, exercise):
        if isinstance(exercise, Exercise):
            self.exercises.append(exercise)
        else:
            raise ValueError("Only instances of Exercise can be added")

    def __repr__(self):
        return f"Workout(exercises={self.exercises})"
