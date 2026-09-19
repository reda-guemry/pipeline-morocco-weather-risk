from src.config import DATA_GOLD_PATH
from src.database import City, sessionFactory, WeatherForecast
from sqlalchemy import select


import pandas as pd 

def load_data_from_csv(filename):
    """
    Load the weather data from a CSV file and return it as a pandas DataFrame.
    """
    
    return pd.read_csv(filename)
    
    
def get_citys_data(df : pd.DataFrame) -> pd.DataFrame :
    """
    Get the citys data from the DataFrame and return it as a pandas DataFrame.
    """
    
    return df[['city', 'timezone', 'lat', 'lng', 'country']].drop_duplicates(ignore_index=True)

def get_wheater_data(df : pd.DataFrame) -> pd.DataFrame :
    """
    Get the citys data from the DataFrame and return it as a pandas DataFrame.
    """
    
    return df.drop(columns=['timezone', 'lat', 'lng', 'country'])


def insert_cities(cities_df : pd.DataFrame) : 

    session = sessionFactory()
    
    
    try : 
        
        
        excitning_name = set (
            session.scalars(
                select(City.name)
            ).all()
        )
        
        
        cities = []

        for _ , row in cities_df.iterrows()  : 
            
            if row['city'] in excitning_name : 
                continue 
                        
            cities.appedn(
                name=row['city'],
                timezone=row['timezone'] ,
                latitude=row['lat'] , 
                longitude=row['lng'] , 
                country=row['country']
        
            )
        
    
    
        session.add_all(cities)
        session.commit()
    except Exception :
        session.rollback()
        raise
    finally : 
        session.close()
        
        
def indsert_wheater_data(wheater_df : pd.DataFrame) : 
    session = sessionFactory()
    
    weather_data = []
     
     
    try :
        
        city_map = dict(
            session.execute(
                select(City.name ,City.id)
            ).all()
        )
        
        for _, row in wheater_df.iterrows() : 
            city_id = city_map.get(row['city'])
            
            if city_id is None : 
                continue
            
            weather_data.append(WeatherForecast(
                city_id=city_id,
                date=row['time'],
                temperature_2m_max=row['temperature_2m_max'],
                temperature_2m_min=row['temperature_2m_min'],
                precipitation_sum=row['precipitation_sum'],
                precipitation_probability_max=row['precipitation_probability_max'],
                windspeed_10m_max=row['windspeed_10m_max'],
                windgusts_10m_max=row['windgusts_10m_max'],
                weathercode=row['weathercode'],
                temperature_category=row['temperature_category'],
                precipitation_category=row['precipitation_category'],
                risk_score=row['risk_score'],
            ))
            
        session.add_all(weather_data)
        session.commit()
    except Exception  : 
        session.rollback()
        raise
    finally : 
        session.close()

def run_loader_pipeline() :
    """
    Load the weather data from a CSV file and return it as a pandas DataFrame.
    """
    
    # Load the data from the CSV file
    df = load_data_from_csv(DATA_GOLD_PATH)
    
    cities_df = get_citys_data(df)
    wheater_data = get_wheater_data(df)
    
    insert_cities(cities_df)
    indsert_wheater_data(wheater_data)
    
    
    

