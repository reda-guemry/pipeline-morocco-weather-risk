from sqlalchemy import create_engine 

from src.config import DATABASE_NAME,  DATABASE_PASSWORD, DATABASE_PORT, DATABASE_USER

# postgres connection string
engine = create_engine(f'postgresql+psycopg2://${DATABASE_USER}:${DATABASE_PASSWORD}@postgres:${DATABASE_PORT}/${DATABASE_NAME}')