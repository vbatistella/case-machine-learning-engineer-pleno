#!/bin/bash
API_URL="http://0.0.0.0:8000/health/"

curl -X GET $API_URL
