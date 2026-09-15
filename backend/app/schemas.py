from datetime import date, time

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    date: date
    time: time