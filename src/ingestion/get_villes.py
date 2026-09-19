import pandas as pd 


def get_villes(data_path) : 
    """
    Get the list of cities from the CSV file.
    """
    try : 
        return pd.read_csv(data_path)
    except Exception as e : 
        print(f"Error reading CSV file: {e}")
        return None