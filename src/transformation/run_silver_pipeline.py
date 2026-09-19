
import pandas as pd

from src.config import DATA_SILVER_PATH
from src.helper import save_dataframe_to_csv

from src.transformation import load_weather, transform_weather, drop_unitile_columns, load_cities, Standardisation

    

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

