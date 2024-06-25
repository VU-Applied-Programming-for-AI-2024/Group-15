from enum import Enum

class BodyPart(Enum):
    BACK = "BACK"
    CARDIO = "CARDIO"
    CHEST = "CHEST"
    LOWER_ARMS = "LOWER_ARMS"
    LOWER_LEGS = "LOWER_LEGS"
    NECK = "NECK"
    SHOULDERS = "SHOULDERS"
    UPPER_ARMS = "UPPER_ARMS"
    UPPER_LEGS = "UPPER_LEGS"
    WAIST = "WAIST"

# Define a mapping of body parts to muscles
BODY_PART_MUSCLES = {
    BodyPart.BACK: ["lats", "traps", "upper back"],
    BodyPart.CARDIO: ["cardiovascular system"],
    BodyPart.CHEST: ["pectorals", "serratus anterior"],
    BodyPart.LOWER_ARMS: ["forearms"],
    BodyPart.LOWER_LEGS: ["calves"],
    BodyPart.NECK: ["levator scapulae"],
    BodyPart.SHOULDERS: ["delts"],
    BodyPart.UPPER_ARMS: ["biceps", "triceps"],
    BodyPart.UPPER_LEGS: ["abductors", "adductors", "hamstrings", "quads"],
    BodyPart.WAIST: ["abs", "spine", "glutes"]
}

class MuscleGroupDistributor:
    def __init__(self, days: int):
        self.days = days

    def distribute_muscle_groups(self):
        if self.days == 2:
            return [
                [BodyPart.CHEST, BodyPart.UPPER_ARMS], 
                [BodyPart.BACK, BodyPart.SHOULDERS], 
                [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS]
            ]
        elif self.days == 3:
            return [
                [BodyPart.CHEST, BodyPart.UPPER_ARMS], 
                [BodyPart.BACK, BodyPart.SHOULDERS], 
                [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS]
            ]
        elif self.days == 4:
            return [
                [BodyPart.CHEST, BodyPart.UPPER_ARMS], 
                [BodyPart.BACK, BodyPart.SHOULDERS], 
                [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS], 
                [BodyPart.LOWER_ARMS, BodyPart.WAIST, BodyPart.CARDIO]
            ]
        elif self.days == 5:
            return [
                [BodyPart.CHEST], 
                [BodyPart.BACK], 
                [BodyPart.UPPER_ARMS, BodyPart.SHOULDERS], 
                [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS], 
                [BodyPart.WAIST, BodyPart.LOWER_ARMS, BodyPart.CARDIO]
            ]
        else:
            raise ValueError("Number of days must be between 2 and 5")

    def get_specific_muscles(self, body_part: BodyPart):
        return BODY_PART_MUSCLES.get(body_part, [])

# Usage example
distributor = MuscleGroupDistributor(4)
muscle_groups_schedule = distributor.distribute_muscle_groups()


