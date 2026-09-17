from sqlalchemy import create_engine 

# postgres connection string
engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/weather_forecast_db', echo=True)