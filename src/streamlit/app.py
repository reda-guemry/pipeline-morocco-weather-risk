from sqlalchemy import select ,func

import streamlit as st
from src.database import (
    City, 
    WeatherForecast,
    sessionFactory
)

session = sessionFactory()

stmt = (
    select(
        func.count(City.id) 
    )
)

nombre_citie = session.scalar(stmt)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Cities", nombre_citie)
col2.metric("Max Temperature", "38.5 °C")
col3.metric("Max Precipitation", "42 mm")
col4.metric("Risk Periods", 12)
col5.metric("Highest Risk City", "Marrakech")

