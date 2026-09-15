from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Appointment
from app.schemas import AppointmentCreate
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

@app.post("/appointments")
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    date_available = await is_date_available(appointment.date)

    if not date_available:
        raise HTTPException(
            status_code=400,
            detail="Data indisponível para agendamento.",
        )

    time_slots = generate_time_slots()

    if appointment.time not in time_slots:
        raise HTTPException(
            status_code=400,
            detail="Horário indisponível para agendamento.",
        )

    occupied_times = get_occupied_times(
        db,
        appointment.date,
    )

    if appointment.time in occupied_times:
        raise HTTPException(
            status_code=400,
            detail="Horário já está ocupado.",
        )

    new_appointment = Appointment(
        date=appointment.date,
        time=appointment.time,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "id": new_appointment.id,
        "date": new_appointment.date,
        "time": new_appointment.time,
    }