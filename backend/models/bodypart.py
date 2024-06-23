from enum import Enum
from typing import List

class BodyPart(Enum):
    BACK = ["lats", "traps", "upper back"]
    CARDIO = ["cardiovascular system"]
    CHEST = ["pectorals", "serratus anterior"]
    LOWER_ARMS = ["forearms"]
    LOWER_LEGS = ["calves"]
    NECK = ["levator scapulae"]
    SHOULDERS = ["delts"]
    UPPER_ARMS = ["biceps", "triceps"]
    UPPER_LEGS = ["abductors", "adductors", "hamstrings", "quads"]
    WAIST = ["abs", "spine", "glutes"]

class MuscleGroupDistributor:
    def __init__(self, days: int):
        self.days = days

    def distribute_muscle_groups(self) -> List[List[BodyPart]]:
        if self.days == 2:
            return [[BodyPart.BACK, BodyPart.CHEST, BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS], 
                    [BodyPart.BACK, BodyPart.CHEST, BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS]]
        elif self.days == 3:
            return [[BodyPart.CHEST, BodyPart.UPPER_ARMS], 
                    [BodyPart.BACK, BodyPart.SHOULDERS], 
                    [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS]]
        elif self.days == 4:
            return [[BodyPart.CHEST, BodyPart.UPPER_ARMS], 
                    [BodyPart.BACK, BodyPart.SHOULDERS], 
                    [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS], 
                    [BodyPart.LOWER_ARMS, BodyPart.WAIST, BodyPart.CARDIO]]
        elif self.days == 5:
            return [[BodyPart.CHEST], 
                    [BodyPart.BACK], 
                    [BodyPart.UPPER_ARMS, BodyPart.SHOULDERS], 
                    [BodyPart.UPPER_LEGS, BodyPart.LOWER_LEGS], 
                    [BodyPart.WAIST, BodyPart.LOWER_ARMS, BodyPart.CARDIO]]
        else:
            raise ValueError("Number of days must be between 2 and 5")
