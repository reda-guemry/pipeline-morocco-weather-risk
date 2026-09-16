

import pandas as pd

from src.config.path import DATA_SILVER_PATH


def load_silver() : 
    """
    Load the silver data from the CSV file.
    """
    try : 
        silver_data = pd.read_csv(DATA_SILVER_PATH)
        return silver_data
    except Exception as e : 
        print(f"Error reading CSV file: {e}")
        return None