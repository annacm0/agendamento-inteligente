from datetime import date, time

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.app import app
from app.database import Base, get_db
from app.models import Appointment
from app.services.availability import get_occupied_times

def test_get_occupied_times():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
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

def test_get_available_times():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.get(
        "/available",
        params={"date": "2026-02-10"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == "2026-02-10"
    assert "08:00:00" in data["available_times"]
    assert "17:00:00" in data["available_times"]

    app.dependency_overrides.clear()
    db.close()

def test_create_appointment():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/appointments",
        json={
            "date": "2026-02-12",
            "time": "10:00",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["date"] == "2026-02-12"
    assert data["time"] == "10:00:00"

    app.dependency_overrides.clear()
    db.close()

def test_create_appointment_when_time_is_occupied():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    appointment = Appointment(
        date=date(2026, 2, 12),
        time=time(10, 0),
    )

    db.add(appointment)
    db.commit()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/appointments",
        json={
            "date": "2026-02-12",
            "time": "10:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Horário já está ocupado."

    app.dependency_overrides.clear()
    db.close()

def test_create_appointment_outside_business_hours():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/appointments",
        json={
            "date": "2026-02-12",
            "time": "18:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Horário indisponível para agendamento."

    app.dependency_overrides.clear()
    db.close()

def test_create_appointment_on_weekend():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/appointments",
        json={
            "date": "2026-02-14",
            "time": "10:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Data indisponível para agendamento."

    app.dependency_overrides.clear()
    db.close()

def test_create_appointment_on_holiday():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.post(
        "/appointments",
        json={
            "date": "2026-02-17",
            "time": "10:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Data indisponível para agendamento."

    app.dependency_overrides.clear()
    db.close()