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
    


def get_lalltinude_data(lat, lon):
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
        response = requests.get(api, params=params, timeout=10)  # Set a timeout en Seconds
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exception.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main() :
    """
    Main function to get weather data for all cities in the CSV file.
    """
    villes = get_villes(data_path)

    for index, ville in villes.iterrows():
        lat = ville.get('lat')
        lon = ville.get('lng')
        # print (ville) 
        # break 
        if lat is not None and lon is not None:
            weather_data = get_lalltinude_data(lat, lon)
            if weather_data is not None:
                print(f"Weather data for {ville.get('city')}: {weather_data}")
                break  # Remove this break if you want to process all cities
            else:
                print(f"Failed to retrieve weather data for {ville.get('city')}.")
        else:
            print(f"Latitude or longitude missing for {ville.get('city')}.")

main()