from src.config import DATA_PATH
from src.ingestion import get_villes 


def load_cities() :
    """
    Load the list of cities from the CSV file.
    """
    return get_villes(DATA_PATH)
    