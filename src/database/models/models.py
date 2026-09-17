from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey, UniqueConstraint

import datetime

class Base(DeclarativeBase):
    pass 



class City(Base) :
    __tablename__ = "cities" 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    timezone: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    
    weather_forecasts: Mapped[list['WeatherForecast']] = relationship(back_populates='city')
    
    
class WeatherForecast(Base) : 
    __tablename__ = 'weather_forecasts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ) , nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    temperature_2m_max: Mapped[float] = mapped_column(nullable=False)
    temperature_2m_min: Mapped[float] = mapped_column(nullable=False)
    precipitation_sum: Mapped[int] = mapped_column(nullable=False)
    precipitation_probability_max: Mapped[int] = mapped_column(nullable=False)
    windspeed_10m_max: Mapped[float] = mapped_column(nullable=False)
    windgusts_10m_max: Mapped[float] = mapped_column(nullable=False)
    weathercode: Mapped[int] = mapped_column(nullable=False)
    temperature_category: Mapped[str | None] 
    precipitation_category: Mapped[str | None] 
    wind_speed_category: Mapped[str | None] 
    is_rainy: Mapped[bool | None] 
    risk_score: Mapped[int | None] 
    forecast_runs: Mapped[datetime.datetime] = mapped_column(nullable=False)
    
    city : Mapped['City'] = relationship(back_populates='weather_forecasts')
    
    __table_args__ = (
        # Add a unique constraint on the combination of city_id and date
        UniqueConstraint('city_id', 'date', name='uix_city_date'), 
    )
    
    

    
    
    