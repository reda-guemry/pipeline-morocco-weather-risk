import json
import requests
import pandas as pd 

api = 'https://api.open-meteo.com/v1/forecast'
data_path = 'data/bronze/ma.csv'


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
        response = session.get(api, params=params, timeout=20)  # Set a timeout en Seconds
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


def save_data_to_json(data, filename) : 
    """
    Save the weather data to a JSON file.
    """
    try : 
        with open(filename, 'w') as f: 
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")
        
        

def main() :
    """
    Main function to get weather data for all cities in the CSV file.
    """
    villes = get_villes(data_path)

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
                data.append(weather_data)
            else:
                print(f"Failed to retrieve weather data for {ville.get('city')}.")
        else:
            print(f"Latitude or longitude missing for {ville.get('city')}.")
            
    save_data_to_json(data, 'data/bronze/weather_data.json')


main()