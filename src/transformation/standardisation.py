
import pandas as pd


def Standardisation(wheater_data : pd.DataFrame) -> pd.DataFrame : 

    wheater_data['time'] = pd.to_datetime(wheater_data['time'] , errors='coerce')
    return wheater_data 
