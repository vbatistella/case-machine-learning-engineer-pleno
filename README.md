# PICPAY CASE: Machine Learning Inference API

## Overview
This repository contains a **FastAPI** application for managing machine learning model predictions, versioning, and inference history. It provides endpoints for:
- Health checks
- Generating predictions using a trained model
- Dynamically loading new models
- Viewing inference history

---

## Features
### 1. Health Check
- **Endpoint**: `/health/`
- Returns the operational status of the API.

### 2. Model Prediction
- **Endpoint**: `/model/predict/`
- Accepts input features as a JSON payload and returns:
  - Prediction score
  - Model version
- Records the prediction, input features, timestamp, and model version in the database.

### 3. Load Model
- **Endpoint**: `/model/load/`
- Accepts `.pkl` files to update the current model used for predictions.

### 4. Inference History
- **Endpoint**: `/model/history/`
- Returns a list of all recorded predictions.

---

## Components
### 1. In-Memory Database
- Implemented using `mongomock`.
- Stores inference data in the `data_capture` collection.
- Provides methods:
  - `add_inference(payload, score, version)`: Adds a new record to the database.
  - `get_history()`: Retrieves all recorded inferences.

### 2. Inference Model
- Manages loading, updating, and predictions using a scikit-learn model.

---

## How to Run
1. Install dependencies:
   ```bash
   make build
   make run
   ```

or simply

```bash
make build-run
```

2. Test endpoints

```bash
curl -X POST "http://0.0.0.0:8000/model/predict/" \
  -H "Content-Type: application/json" \
  -d "{
    "sched_dep_time": 1059,
    "sched_arr_time": 1209,
    "distance": 284,
    "clouds": 93,
    "pres": 1011,
    "wind_spd": 5.8,
    "precip": 0.0,
    "snow": 0.0
    }"
```

### Directory Structure
```
docs/                       # Arquitecture images
notebook/
├── data/                   # Data folder
├── download_weather.py     # Download weather data
├── Notebook.ipynb          # Question Answers and model training
src/
├── curl_scripts/           # Scripts for endpoint local testing
├── model/                  # Folder for model pickle storage
├── database.py             # In-memory database implementation
├── model.py                # Model management and inference logic
├── main.py                 # FastAPI application
Dockerfile                  # Dockerfile for conteinerization
Makefile                    # Makefile for faster build and run
requirements.txt            # Python requirements for application
README.md                   # Summary documentation
```