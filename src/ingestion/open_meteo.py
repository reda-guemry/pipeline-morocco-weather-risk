import json
import requests
import pandas as pd 

from src.config import API, DATA_PATH, SAVE_WHEATHER_DATA_PATH
from src.helper import save_data_to_json


def get_villes(data_path) : 
    """
    Get the list of cities from the CSV file.
    """
    try : 
        return pd.read_csv(data_path)
    except Exception as e : 
        print(f"Error reading CSV file: {e}")
        return None
    



def get_weather_data(lat, lon, session=requests.Session()) :
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



        

def run_bronze_pipeline() :
    """
    Main function to get weather data for all cities in the CSV file.
    """
    villes = get_villes(DATA_PATH)

    data = []
    
    for index, ville in villes.iterrows():
        lat = ville.get('lat')
        lon = ville.get('lng')
        
        # print (ville) 
        # break 
        if lat is not None and lon is not None:
            print(f"Fetching weather for {ville.get('city')}...")
            weather_data = get_weather_data(lat, lon)
            if weather_data is not None:
                weather_data['city'] = ville.get('city')
                data.append(weather_data)
            else:
                print(f"Failed to retrieve weather data for {ville.get('city')}.")
        else:
            print(f"Latitude or longitude missing for {ville.get('city')}.")
            
    save_data_to_json(data, SAVE_WHEATHER_DATA_PATH)
    
    
