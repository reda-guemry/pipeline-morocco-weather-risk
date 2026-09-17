from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import UniqueConstraint

from src.database import Base


class City(Base) :
    __tablename__ = "cities" 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    timezone: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    
    weather_forecasts: Mapped[list['WeatherForecast']] = relationship(back_populates='city')
    
    __table_args__ = (
        UniqueConstraint('name', name='city_name_unique'), 
        
    )