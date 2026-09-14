from datetime import datetime, time

OPENING_TIME = time(8, 0)
CLOSING_TIME = time(18, 0)
APPOINTMENT_DURATION_HOURS = 1

def generate_time_slots() -> list[time]:
    slots = []

    current_hour = OPENING_TIME.hour

    while current_hour < CLOSING_TIME.hour:
        slots.append(time(current_hour, 0))
        current_hour += APPOINTMENT_DURATION_HOURS

    return slots