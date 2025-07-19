import os
import time
import pytest

from fastapi.testclient import TestClient
from main import app

from config import test_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Task


engine = create_engine(test_settings.DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def setup_and_teardown():
    db = TestingSessionLocal()
    db.query(Task).delete()
    db.add(Task(task_id="task_001", status="In Progress", deadline_minutes=15))
    db.commit()
    db.close()
    yield 

def teardown_module(module):
    
    engine.dispose()
    time.sleep(0.5) 
    if os.path.exists("test_task_db.sqlite"):
        os.remove("test_task_db.sqlite")


def test_extend_deadline_with_minutes(client):
    response = client.post("/api/tasks/task_001/extend?minutes=40")
    assert response.status_code == 200
    assert response.json()["message"] == "Deadline extended to 40 minutes"

def test_extend_deadline_without_minutes(client):
    response = client.post("/api/tasks/task_001/extend")
    assert response.status_code == 200
    assert "Deadline extended to" in response.json()["message"]

def test_change_status(client):
    response = client.post("/api/tasks/task_001/status/Success")
    assert response.status_code == 200
    assert response.json()["message"] == "Status updated to 'Success'"
