

import pandas as pd


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
    
    