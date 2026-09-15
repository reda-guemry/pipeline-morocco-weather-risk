import json

import pandas as pd

from src.ingestion.open_meteo import get_villes 
from src.config import DATA_PATH,SAVE_WHEATHER_DATA_PATH

def load_cities() :
    """
    Load the list of cities from the CSV file.
    """
    villes = get_villes(DATA_PATH)
    return villes


def load_weather() -> list[dict] : 
    """
    Load the weather data from the JSON file.
    """
    try : 
        with open(SAVE_WHEATHER_DATA_PATH, "r") as f : 
            weather_data = json.load(f)
        return weather_data
    except Exception as e : 
        print(f"Error reading JSON file: {e}")
        return None
    
    


    
def transform_weather(wheater_data: list[dict]) -> pd.DataFrame:  
    dataframe = [] 
    
    
    for data in wheater_data :
        daily = data['daily'] 
        
        pdframe = pd.DataFrame(daily) 
        
        pdframe['latitude'] = data['latitude']
        pdframe['longitude'] = data['longitude']
        pdframe['timezone'] = data['timezone']
        pdframe['city'] = data['city']
        
        dataframe.append(pdframe)
        
    return pd.concat(dataframe, ignore_index=True)

    

def run_bronze_pipeline() : 
    wheater_data = load_weather()
    
    wheather_df = transform_weather(wheater_data)

    if wheather_df is None :
        print("No weather data to transform.")
        return
    
    

run_bronze_pipeline()