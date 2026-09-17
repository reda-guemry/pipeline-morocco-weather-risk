from sqlalchemy.orm import sessionmaker

from src.database import engine 


sessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)