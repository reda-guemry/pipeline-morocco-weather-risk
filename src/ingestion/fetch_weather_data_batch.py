
import json
import requests

from src.config import API

DAILY_VARIABLES = [
    'temperature_2m_max',    # Maximum Temperature
    'temperature_2m_min',    # Minimum Temperature
    'precipitation_sum',     # Precipitation Sum
    'precipitation_probability_max',  # Precipitation Probability Maximum
    'windspeed_10m_max',     # Maximum Wind Speed
    'windgusts_10m_max',     # Maximum Wind Gusts
    'weathercode',           # Weather Code
]


def fetch_weather_data_batch(lats, lons, session=requests.Session()):
    """
    Get the weather data for many cities in ONE request.
    """
    params = {
        'latitude': ','.join(str(lat) for lat in lats),
        'longitude': ','.join(str(lon) for lon in lons),
        'daily': DAILY_VARIABLES,
        'timezone': 'Africa/Casablanca',
    }

    try:
        response = session.get(API, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
