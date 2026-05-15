import random


def roll_detection(detection_chance: int) -> bool:
    if detection_chance <= 0:
        return False

    if detection_chance >= 100:
        return True

    return random.randint(1, 100) <= detection_chance