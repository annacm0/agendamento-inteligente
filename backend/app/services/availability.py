from datetime import date, time

from app.services.holidays import get_holidays
from sqlalchemy.orm import Session

from app.models import Appointment

async def is_date_available(selected_date: date) -> bool:
    if selected_date.weekday() >= 5:
        return False

    holidays = await get_holidays()

    return selected_date.isoformat() not in holidays

def get_occupied_times(
    db: Session,
    selected_date: date,
) -> set[time]:
    appointments = (
        db.query(Appointment)
        .filter(Appointment.date == selected_date)
        .all()
    )

    return {appointment.time for appointment in appointments}