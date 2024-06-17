from day import Day
from workout import Workout

class Schedule:
    def __init__(self):
        self.schedule = {day: None for day in Day}

    def set_workout(self, day, workout):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")
        if not isinstance(workout, Workout):
            raise ValueError("Workout must be an instance of the Workout class")
        self.schedule[day] = workout

    def get_workout(self, day):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")
        return self.schedule.get(day)

    def __repr__(self):
        return f"Schedule(schedule={self.schedule})"
