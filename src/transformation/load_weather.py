
from src.config import SAVE_WHEATHER_DATA_PATH
import json


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
    