import json

import pandas as pd

from ingestion.run_bronze_pipeline import get_villes 
from src.config import DATA_PATH,SAVE_WHEATHER_DATA_PATH, DATA_SILVER_PATH
from src.helper import save_dataframe_to_csv


def load_cities() :
    """
    Load the list of cities from the CSV file.
    """
    return get_villes(DATA_PATH)
    

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
        pdframe['timezone'] = data['timezone_abbreviation']
        pdframe['city'] = data['city']
        
        dataframe.append(pdframe)
        
    return pd.concat(dataframe, ignore_index=True)

def Standardisation(wheater_data : pd.DataFrame) -> pd.DataFrame : 

    wheater_data['time'] = pd.to_datetime(wheater_data['time'] , errors='coerce')
    return wheater_data 


def quality_check(wheater_data : pd.DataFrame) :
    """
    Perform quality checks on the weather data.
    Returns True if the data passes the checks, False otherwise.
    """
    
    
    print(wheater_data.duplicated().sum()) # 0 duplicates
    
    print(wheater_data.isna().sum()) # 0 missing values
    
    print(wheater_data.dtypes) # Check data types
    
    print(wheater_data['precipitation_probability_max'].between(0 , 100).all()) # Check if all values are between 0 and 100
    


    print((wheater_data['temperature_2m_max'] < wheater_data['temperature_2m_min']).sum()) # Check if there are any rows where max temperature is less than min temperature
        
    print((wheater_data['windgusts_10m_max'] < wheater_data['windspeed_10m_max']).sum()) # Check if there are any rows where max wind gusts is less than max wind speed
    
    print(wheater_data["latitude"].between(-90, 90).all())
    print(wheater_data["longitude"].between(-180, 180).all())
    
    print((wheater_data.groupby('city').size() == 7).sum())   
    
    
    
def drop_unitile_columns(dataframe : pd.DataFrame) -> pd.DataFrame : 
    """
    Drop the meta columns from the DataFrame.
    """
    return dataframe.drop(columns=['longitude' , 'latitude' , 'iso2', 'capital' , '_merge' , 'admin_name'])


def run_silver_pipeline() : 
    wheater_data = load_weather()
    
    wheather_df = transform_weather(wheater_data)

    
    # quality_check(wheather_df)
        
    wheather_df_standariser = Standardisation(wheather_df)
    
    
    total_citys = load_cities() 
    
    # print(wheather_df_standariser.head())
    
    join_data = wheather_df_standariser.merge(
        total_citys,
        on=['city'],
        how='left',
    )
    
    final_data = drop_unitile_columns(join_data) 
    
    # print(final_data.columns) # Check if all cities have 7 days of data
    
    
    save_dataframe_to_csv(final_data, DATA_SILVER_PATH)



run_silver_pipeline()