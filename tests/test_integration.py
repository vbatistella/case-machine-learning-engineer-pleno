import pytest
from fastapi.testclient import TestClient
from src.main import app  # Assuming your FastAPI app is in src/main.py

@pytest.fixture(scope="module")
def client():
    """
    Create a TestClient for the FastAPI app to make requests during testing.
    """
    with TestClient(app) as client:
        yield client

def test_health_check(client):
    """
    Test the /health endpoint to ensure it returns a status of 'ok'.
    """
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict(client):
    """
    Test the /model/predict endpoint with valid input to check if the prediction works.
    """
    payload = {
        "sched_dep_time": 1059,
        "sched_arr_time": 1209,
        "distance": 284,
        "clouds": 93,
        "pres": 1011,
        "wind_spd": 5.8,
        "precip": 0.0,
        "snow": 0.0
    }

    response = client.post("/model/predict/", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert "score" in response_data
    assert "model_version" in response_data

def test_load_model(client):
    """
    Test the /model/load endpoint to load a new model from a .pkl file.
    """
    with open("src/model/model_2.pkl", "rb") as model_file:
        response = client.post("/model/load/", files={"file": ("model.pkl", model_file, "application/octet-stream")})

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Model loaded successfully"}

def test_get_history(client):
    """
    Test the /model/history endpoint to retrieve past prediction history.
    """
    response = client.get("/model/history/")
    assert response.status_code == 200
    response_data = response.json()
    assert "history" in response_data
    assert isinstance(response_data["history"], list)
