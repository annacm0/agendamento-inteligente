from datetime import date

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Appointment
from app.services.availability import (
    get_occupied_times,
    is_date_available,
)
from app.services.schedule import generate_time_slots

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/available")
async def get_available_times(
    date: date,
    db: Session = Depends(get_db),
):
    date_available = await is_date_available(date)

    if not date_available:
        return {"date": date, "available_times": []}

    time_slots = generate_time_slots()
    occupied_times = get_occupied_times(db, date)

    available_times = [
        slot for slot in time_slots
        if slot not in occupied_times
    ]

    return {
        "date": date,
        "available_times": available_times,
    }