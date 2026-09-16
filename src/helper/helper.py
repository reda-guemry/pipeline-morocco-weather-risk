
import json
import pandas as pd
from pathlib import Path

def save_data_to_json(data, filename) : 
    """
    Save the weather data to a JSON file.
    """
    try : 
        with open(filename, 'w') as f: 
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")
        
        
        


def save_dataframe_to_csv(data, filename) : 
    """
    Save the weather data to a CSV file.
    """
    try : 
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True) # Create parent directories if they don't exist
        data.to_csv(filename, index=False)
    except Exception as e:
        print(f"Error saving data to CSV file: {e}")
    
