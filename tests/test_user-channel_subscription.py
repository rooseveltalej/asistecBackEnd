from fastapi.testclient import TestClient
from app import app
from database import Base, engine
import pytest

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def create_areas():
    # Crear área informativa
    res_info = client.post("/api/areas/create", json={"area_name": "DEVESA", "is_major": False})
    assert res_info.status_code == 201
    devesa = res_info.json()

    # Crear área mayor
    res_major = client.post("/api/areas/create", json={"area_name": "Escuela de Ingeniería en Computación", "is_major": True})
    assert res_major.status_code == 201
    eic = res_major.json()

    return {"informative": devesa, "major": eic}

@pytest.fixture(scope="module")
def create_user(create_areas):
    user_data = {
        "name": "Carlos",
        "lastname": "Ramírez",
        "mail": "carlos.ramirez@example.com",
        "password": "testpass",
        "area_id": create_areas["major"]["area_id"]
    }
    res = client.post("/api/users/user_create", json=user_data)
    assert res.status_code == 201
    return user_data  # para login después

@pytest.fixture(scope="module")
def user_id(create_user):
    res = client.get("/api/users/user_login", params={
        "mail": create_user["mail"],
        "password": create_user["password"]
    })
    assert res.status_code == 200
    return res.json()["user_id"]

def test_create_informative_area(create_areas):
    assert create_areas["informative"]["area_name"] == "DEVESA"

def test_create_major_area(create_areas):
    assert create_areas["major"]["area_name"] == "Escuela de Ingeniería en Computación"

def test_create_user_in_major_area(create_user):
    assert create_user["area_id"] > 0

def test_user_should_be_subscribed_to_informative_and_major_channels(user_id):
    res = client.get("/api/channels/subscribed_channels", params={"user_id": user_id})
    assert res.status_code == 200
    subs = res.json()
    assert len(subs) == 2
    names = [s["channel_name"] for s in subs]
    assert any("DEVESA" in n for n in names)
    assert any("Escuela de Ingeniería en Computación" in n for n in names)
