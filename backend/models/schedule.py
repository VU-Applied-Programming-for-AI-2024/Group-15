from models.day import Day
from models.exercise import Exercise
from models.workout_exercise import WorkoutExercise
from models.workout import Workout
import re 

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
                            exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=name, target="unknown")
                            workout.add_exercise(WorkoutExercise(exercise_obj, sets, reps))
                        else:
                            exercise_obj = Exercise(body_part="unknown", equipment="unknown", gif_url="unknown", exercise_id="unknown", name=exercise.strip(), target="unknown")
                            workout.add_exercise(WorkoutExercise(exercise_obj, 0, ""))
        if current_day and workout:
            self.schedule[day_mapping[current_day]] = workout

    def get_workout(self, day):
        if not isinstance(day, Day):
            raise ValueError("Day must be an instance of the Day enum")
        return self.schedule.get(day)

    def __repr__(self):
        return f"Schedule(schedule={self.schedule})"
