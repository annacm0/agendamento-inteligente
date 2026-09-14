from datetime import date, time

from sqlalchemy import Date, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)