#!/bin/bash
MODEL_FILE_PATH="src/model/model_2.pkl"
API_URL="http://0.0.0.0:8000/model/load/"


curl -X 'POST' \
  "$API_URL" \
  -F "file=@$MODEL_FILE_PATH"
