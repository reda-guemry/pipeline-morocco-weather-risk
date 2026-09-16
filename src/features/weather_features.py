import pandas as pd

from src.features import load_silver




def categorical_whetaer_temperature(silver_data: pd.DataFrame) -> pd.DataFrame: 
    """
    Load the silver data and return a DataFrame with categorical weather temperature.
    """
    
    if silver_data is None : 
        print("Failed to load silver data.")
        return None

    # Define temperature categories
    
    bins = [-float('inf'), 10, 20, 30 , 35, float('inf')]
    labels = ['Cold', 'Mild', 'Warm', 'Hot', 'Very Hot']
    
    
    silver_data['temperature_category'] = pd.cut(
        silver_data['temperature_2m_max'],
        bins=bins,
        labels=labels
    )
    
    return silver_data

def categorical_précipitations(silver_data: pd.DataFrame) -> pd.DataFrame: 
    """
    Load the silver data and return a DataFrame with categorical weather precipitation.
    """
    
    if silver_data is None : 
        print("Failed to load silver data.")
        return None

    # Define precipitation categories
    
    bins = [-float('inf'), 0, 2, 8 , 20, float('inf')]
    labels = ['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain', 'Very Heavy Rain']
    
    
    silver_data['precipitation_category'] = pd.cut(
        silver_data['precipitation_sum'],
        bins=bins,
        labels=labels
    )
    
    return silver_data


def categorical_wind_speed(silver_data: pd.DataFrame) -> pd.DataFrame:
    """
    Load the silver data and return a DataFrame with categorical weather wind speed.
    """
    
    if silver_data is None : 
        print("Failed to load silver data.")
        return None

    # Define wind speed categories
    
    bins = [-float('inf'), 10, 20, 30, 40, float('inf')]
    labels = ['Calm', 'Breeze', 'Windy', 'Strong Wind', 'Gale']
    
    
    silver_data['wind_speed_category'] = pd.cut(
        silver_data['windspeed_10m_max'],
        bins=bins,
        labels=labels
    )
    
    return silver_data

def add_is_rainy_column(silver_data: pd.DataFrame) -> pd.DataFrame:
    """
    Load the silver data and return a DataFrame with an additional column indicating if it is rainy or not.
    """
    
    if silver_data is None : 
        print("Failed to load silver data.")
        return None

    # Add a new column 'is_rainy' based on precipitation_sum
    silver_data['is_rainy'] = silver_data['precipitation_sum'] > 0
    
    return silver_data