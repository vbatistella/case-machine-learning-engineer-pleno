import pytest
from datetime import datetime, timezone
from mongomock import MongoClient
from src.database import InMemoryDatabase

@pytest.fixture
def mock_db():
    # Clear DB for isolation
    db = InMemoryDatabase()
    db._instance["data_capture"].drop()
    return db

def test_add_inference(mock_db):
    """
    Test simple inference insert on db.
    """
    payload = {"feature1": 5.2, "feature2": 3.1}
    score = 10.5
    version = 1.0

    mock_db.add_inference(payload, score, version)

    history = mock_db.get_history()

    assert len(history) == 1
    inference = history[0]
    assert inference["features"] == payload
    assert inference["score"] == score
    assert "datetime" in inference
    assert inference["model"] == version

def test_get_history(mock_db):
    """
    Test get history for multiple inferences.
    """
    payload1 = {"feature1": 1.0, "feature2": 2.0}
    score1 = 7.2
    version1 = 1.1
    payload2 = {"feature1": 4.3, "feature2": 5.1}
    score2 = 8.4
    version2 = 1.2

    mock_db.add_inference(payload1, score1, version1)
    mock_db.add_inference(payload2, score2, version2)

    history = mock_db.get_history()


    assert len(history) == 2

    inference1 = history[0]
    assert inference1["features"] == payload1
    assert inference1["score"] == score1
    assert inference1["model"] == version1

    inference2 = history[1]
    assert inference2["features"] == payload2
    assert inference2["score"] == score2
    assert inference2["model"] == version2

def test_empty_history(mock_db):
    """
    Test get history for no inferences added.
    """
    history = mock_db.get_history()
    assert history == []

