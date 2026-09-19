

from src.ingestion import get_villes, fetch_weather_data

from src.config import DATA_PATH, SAVE_WHEATHER_DATA_PATH
from src.helper import save_data_to_json    


        

def run_bronze_pipeline() :
    """
    Main function to get weather data for all cities in the CSV file.
    """
    villes = get_villes(DATA_PATH)
    
    print(f"Retrieved {len(villes)} cities from the CSV file.")

    data = []
    
    for index, ville in villes.iterrows():
        lat = ville.get('lat')
        lon = ville.get('lng')
        
        # print (ville) 
        # break 
        if lat is not None and lon is not None:
            print(f"Fetching weather data for {ville.get('city')}...")
            weather_data = fetch_weather_data(lat, lon)
            if weather_data is not None:
                weather_data['city'] = ville.get('city')
                data.append(weather_data)
            else:
                print(f"Failed to retrieve weather data for {ville.get('city')}.")
        else:
            print(f"Latitude or longitude missing for {ville.get('city')}.")
            
    save_data_to_json(data, SAVE_WHEATHER_DATA_PATH)
    
    
