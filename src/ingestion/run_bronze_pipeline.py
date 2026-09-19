from src.ingestion import get_villes
from src.ingestion.fetch_weather_data_batch import fetch_weather_data_batch

from src.config import DATA_PATH, SAVE_WHEATHER_DATA_PATH
from src.helper import save_data_to_json


def run_bronze_pipeline():
    """
    Get weather data for all cities in the CSV file with ONE request.
    """
    villes = get_villes(DATA_PATH)

    valid_cities = villes[villes['lat'].notna() & villes['lng'].notna()]

    if valid_cities.empty:
        print("No valid cities with latitude/longitude.")
        return

    print(f"Fetching weather data for {len(valid_cities)} cities ")

    responses = fetch_weather_data_batch(
        valid_cities['lat'].tolist(),
        valid_cities['lng'].tolist(),
    )

    if responses is None:
        print("Failed to retrieve weather data.")
        return
    
    
    data = []
    for response, (_, ville) in zip(responses, valid_cities.iterrows()):
        response['city'] = ville['city']
        data.append(response)

    save_data_to_json(data, SAVE_WHEATHER_DATA_PATH)
    print(f"Saved weather data for {len(data)} cities.")