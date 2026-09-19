from src.features import (
    load_silver,
    categorical_précipitations, 
    categorical_wind_speed,
    categorical_whetaer_temperature, 
    add_is_rainy_column, 
    risk_score
)
from src.helper import save_dataframe_to_csv
from src.config import DATA_GOLD_PATH


def run_gold_pipeline() : 
    
    data = load_silver()

    if data is None :
        print("Failed to load silver data.")
        return None

    data = categorical_whetaer_temperature(data)
    data = categorical_précipitations(data)
    data = categorical_wind_speed(data)
    data = add_is_rainy_column(data)
    data = risk_score(data)
    
    
    save_dataframe_to_csv(data, DATA_GOLD_PATH)

    