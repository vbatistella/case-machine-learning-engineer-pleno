#!/bin/bash
API_URL="http://0.0.0.0:8000/model/predict/"

PAYLOAD='{
    "sched_dep_time": 1059,
    "sched_arr_time": 1209,
    "distance": 284,
    "clouds": 93,
    "pres": 1011,
    "wind_spd": 5.8,
    "precip": 0.0,
    "snow": 0.0
}'

# Sending the POST request
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
