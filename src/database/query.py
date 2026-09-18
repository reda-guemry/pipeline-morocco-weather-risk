from src.database import City, sessionFactory, WeatherForecast
from sqlalchemy import select, func


def select_most_temperature() :
    session = sessionFactory ()
    
    stmt = (
        select(WeatherForecast)
        .order_by(WeatherForecast.temperature_2m_max.desc())
        .limit(1)
    )
    
    weather = session.scalar(stmt)
    print(weather.city.name)

def select_most_precipation(): 
    session = sessionFactory()

    stmt = (
        select(WeatherForecast)
        .order_by(WeatherForecast.precipitation_sum.desc())
        .limit(1)
    )
    result = session.scalar(stmt)
    print(result.city.name)

def most_avrg_risk() : 
    session = sessionFactory()

    stmt = (
        select(
            City.name , 
            func.avg(WeatherForecast.risk_score).label('avg_risk_value')
        )
        .join(
            City, 
            City.id == WeatherForecast.city_id
        )
        .group_by(City.id )
        .order_by(func.avg(WeatherForecast.risk_score).desc())
        .limit(1)
    )
    result = session.execute(stmt)
    
    result = session.execute(stmt).first()

    
    print(result.name, result.avg_risk_value)

    
    
def most_day_risk() :
    session = sessionFactory()
    
    stmt = (
        select(
            WeatherForecast.date , 
            WeatherForecast.risk_score
        )
        .order_by(WeatherForecast.risk_score.desc())
        .limit(1)
    )
    
    result = session.execute(stmt).first()
    print(result.date, result.risk_score)


def most_day_risk() :
    session = sessionFactory()
    
    ranked = (
        select(
            City.name ,
            WeatherForecast.date , 
            WeatherForecast.risk_score , 
            func.row_number().over(
                partition_by=City.id ,
                order_by=WeatherForecast.risk_score.desc()      
            ).label('risk_rank')
        )
        .join(
            City, 
            WeatherForecast.city_id == City.id
        )
        .subquery()
    )
    
    stmt = (
        select(
            ranked.c.name,
            ranked.c.date ,
            ranked.c.risk_score
        )
        .where(ranked.c.risk_rank == 1)
    )
    
    result = session.execute(stmt)
    
    for row in result : 
        print(
            row.name,
            row.date,
            row.risk_score
        )


