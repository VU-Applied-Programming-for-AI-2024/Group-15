class FavoriteSchedule:
    def __init__(self, schedule, schedule_name, email):
        self.schedule = schedule
        self.schedule_name = schedule_name
        self.email = email

    def __str__(self):
        return f"FavoriteSchedule(schedule_name='{self.schedule_name}', email='{self.email}')"