
import json
import requests

from src.config import API




def fetch_weather_data(lat, lon, session=requests.Session()) :
    """
    Get the weather data for a given latitude and longitude.
    """
    
    
    params = {
        'latitude' : lat,
        'longitude' : lon,
        'daily' : [
            'temperature_2m_max', # Maximum Temperature          
            'temperature_2m_min',  # Minimum Temperature
            'precipitation_sum', # Precipitation Sum 
            'precipitation_probability_max', # Precipitation Probability Maximum
            'windspeed_10m_max', # Maximum Wind Speed
            'windgusts_10m_max', # Maximum Wind Gusts
            'weathercode', # Weather Code
        ],
        'timezone' : 'Africa/Casablanca'
    
    }

    try : 
        response = session.get(API, params=params, timeout=20)  # Set a timeout en Seconds
        response.raise_for_status()  # Raise an error for bad responses
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
