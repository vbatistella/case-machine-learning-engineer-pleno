import logging
from datetime import datetime, timedelta
import requests
import time
import json


def get_weather_data(latitude, longitude, start_date, end_date, wait_time=1, retries=3):
    weatherbit_key = 'API_KEY'
    url = 'https://api.weatherbit.io/v2.0/history/daily'
    params = {
        'lat': latitude,
        'lon': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'key': weatherbit_key,
    }
    headers = {
        'Accept': 'application/json',
    }

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                if "data" in data:
                    return data["data"]
                else:
                    logging.error(f"Unexpected API response structure: {data}")
                    return []

            elif response.status_code == 429:
                # Handle rate limiting
                retry_after = int(response.headers.get("Retry-After", wait_time))
                logging.warning(f"Rate limited (429). Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            
            else:
                logging.error(f"API returned status code {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        except ValueError as e:
            logging.error(f"JSON decoding failed: {e}")

        # Wait before retrying on non-429 errors
        time.sleep(wait_time)
        attempt += 1

    logging.error("All retry attempts failed.")
    return []

def generate_date_ranges(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        yield current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")
        current_date = next_date

def fetch_yearly_weather_data(airport_dict):
    weather_data = []
    for airport in airport_dict:
        latitude = airport_dict[airport]["latitude"]
        longitude = airport_dict[airport]["longitude"]
        print(f"Fetching data for airport: {airport}")

        for start_date, end_date in generate_date_ranges(2013):
            print(f"Fetching data for {start_date} to {end_date}...")
            day_data = get_weather_data(latitude, longitude, start_date, end_date)
            if day_data:
                for entry in day_data:
                    entry["airport"] = airport
                weather_data.extend(day_data)

    return weather_data

airport_dict = {'LGA': {'latitude': 40.777199, 'longitude': -73.872597}, 'EWR': {'latitude': 40.692501, 'longitude': -74.168701}, 'JFK': {'latitude': 40.639801, 'longitude': -73.7789}}
weather_data = fetch_yearly_weather_data(airport_dict)

output_file = "weather_data.json"
with open(output_file, "w") as json_file:
    json.dump(weather_data, json_file, indent=4)
