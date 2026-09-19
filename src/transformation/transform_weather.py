
import pandas as pd

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
