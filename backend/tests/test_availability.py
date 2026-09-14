from datetime import date, time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Appointment
from app.services.availability import get_occupied_times


def test_get_occupied_times():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    appointment = Appointment(
        date=date(2026, 2, 10),
        time=time(10, 0),
    )

    db.add(appointment)
    db.commit()

    occupied_times = get_occupied_times(
        db,
        date(2026, 2, 10),
    )

    assert time(10, 0) in occupied_times
    assert time(11, 0) not in occupied_times

    db.close()