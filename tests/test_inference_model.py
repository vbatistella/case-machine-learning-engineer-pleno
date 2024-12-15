import pytest
from src.model import InferenceModel, load_model_path

MODEL_1_PATH = "src/model/model.pkl"
MODEL_2_PATH = "src/model/model_2.pkl"

def test_load_model_path():
    """
    Test the load_model_path function with both model files
    """
    model = load_model_path(MODEL_1_PATH)
    assert model is not None
    assert "x_scaler" in model
    assert "model" in model
    assert "y_scaler" in model

def test_inference_success_model():
    """
    Test the inference method with the first model
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
    model = InferenceModel()
    result = model.inference(payload)

    assert result is not None
    assert isinstance(result, float)

def test_update_model():
    """
    Test the update_model method with a new model
    """
    with open(MODEL_2_PATH, "rb") as file:
        new_model_data = file.read()

    model = InferenceModel()
    version_before = model.get_version()

    assert version_before == 1.0

    result = model.update_model(new_model_data)
    version_after = model.get_version()

    assert version_after > version_before
    assert version_after == 2.0

    assert result == {"status": "ok", "message": "Model loaded successfully"}
    assert model._model is not None


def test_inference_success_second_model():
    """
    Test the inference method with the second model
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
    model = InferenceModel()
    result = model.inference(payload)

    assert result is not None
    assert isinstance(result, float)


def test_inference_model_not_loaded():
    """
    Test the inference method when the model is not loaded
    """
    model = InferenceModel()
    model._model = None
    with pytest.raises(ValueError, match="Model is not loaded."):
        model.inference({"sched_dep_time": 1059})
