from fastapi import FastAPI, File, UploadFile, HTTPException
from src.database import InMemoryDatabase
from src.model import InferenceModel
import uvicorn

app = FastAPI()

@app.get("/health/", status_code=200, tags=["health"], summary="Health check")
async def health():
    """
    Health check endpoint to monitor the status of the API.

    Returns:
        dict: A dictionary with a key "status" set to "ok" if the server is running fine.
    """
    return {"status": "ok"}

@app.post("/model/predict/", status_code=200, tags=["prediction"], summary="Model prediction")
async def predict(payload: dict):
    """
    Predicts the outcome based on the provided input data..

    Args:
        payload (dict): A dictionary containing the input features for prediction.
                         The keys and values should match the expected format of the model.
                         Example:
                         {
                             "sched_dep_time": 1059,      # Scheduled departure time (in HHMM format)
                             "sched_arr_time": 1209,      # Scheduled arrival time (in HHMM format)
                             "distance": 284,             # Distance of the flight in miles
                             "clouds": 93,                # Cloud cover percentage
                             "pres": 1011,                # Atmospheric pressure in hPa
                             "wind_spd": 5.8,             # Wind speed in mph
                             "precip": 0.0,               # Precipitation amount in inches
                             "snow": 0.0                  # Snow amount in inches
                         }

    Returns:
        dict: A dictionary containing the predicted score.
    """
    model = InferenceModel()
    y = model.inference(payload)
    version = model.get_version()

    db = InMemoryDatabase()
    db.add_inference(payload, y, version)

    return {"score": y, "model_version": version}

@app.post("/model/load/", status_code=200, tags=["model"], summary="Load model")
async def load_model(file: UploadFile = File(...)):
    """
    Loads a new model from the uploaded .pkl file.

    Args:
        file (UploadFile): The .pkl file containing the pre-trained model. This file is uploaded
                           through the API request.

    Returns:
        dict: A dictionary containing the status of the model loading process.
    """
    if not file.filename.endswith(".pkl"):
        raise HTTPException(status_code=400, detail="Only .pkl files are supported.")
    
    contents = await file.read()
    model = InferenceModel()
    
    try:
        result = model.update_model(contents)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/model/history/", status_code=200, tags=["history"], summary="Check last predictions")
async def history():
    """
    Retrieves the history of the last predictions made by the model.
    
    Returns:
        dict: A dictionary containing a list of the last prediction records.
    """
    db = InMemoryDatabase()
    history = db.get_history()
    return {"history": history}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")