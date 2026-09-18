from sqlalchemy import select ,func

import streamlit as st
from src.database import (
    City, 
    WeatherForecast,
    sessionFactory
)

session = sessionFactory()

nombre_citie = session.scalar(
    select(
        func.count(City.id) 
    )
)

max_temperature = session.scalar(
    select(
        func.max(WeatherForecast.temperature_2m_max)
    )
)

max_precipitation = session.scalar(
    select(
        func.max(WeatherForecast.precipitation_sum)
    )
)

nombre_periodes_risque = session.scalar(
    select(
        func.count(WeatherForecast.id)
    )
    .where(WeatherForecast.risk_score > 0)
)

ville_risque_eleve = session.scalar(
    select(City.name)
    .join(WeatherForecast, WeatherForecast.city_id == City.id)
    .order_by(WeatherForecast.risk_score.desc())
    .limit(1)
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Cities", nombre_citie)
col2.metric("Max Temperature", f"{max_temperature} °C")
col3.metric("Max Precipitation", f"{max_precipitation} mm")
col4.metric("Risk Periods", nombre_periodes_risque)
col5.metric("Highest Risk City", ville_risque_eleve)

