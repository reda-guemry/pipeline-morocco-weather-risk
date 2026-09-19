from datetime import date

import pandas as pd
import streamlit as st
from sqlalchemy import select

from src.database import City, WeatherForecast, sessionFactory

# A period counts as "at risk" when the simple risk score reaches one
# clearly present hazard: 35C+ heat, 8mm+ rain or strong wind (= 25 pts).
RISK_THRESHOLD = 25


@st.cache_data(ttl=600, show_spinner=False)
def load_weather_data():
    """
    Load weather forecasts joined with city names from the database.
    """
    session = sessionFactory()
    try:
        rows = session.execute(
            select(
                City.name.label("city"),
                WeatherForecast.date,
                WeatherForecast.temperature_2m_max,
                WeatherForecast.temperature_2m_min,
                WeatherForecast.precipitation_sum,
                WeatherForecast.precipitation_probability_max,
                WeatherForecast.windspeed_10m_max,
                WeatherForecast.windgusts_10m_max,
                WeatherForecast.weathercode,
                WeatherForecast.is_rainy,
                WeatherForecast.risk_score,
            )
            .join(City, City.id == WeatherForecast.city_id)
        ).all()
    finally:
        session.close()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=[
        "city", "date", "temperature_2m_max", "temperature_2m_min",
        "precipitation_sum", "precipitation_probability_max",
        "windspeed_10m_max", "windgusts_10m_max", "weathercode",
        "is_rainy", "risk_score",
    ])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


st.set_page_config(page_title="Bulletin météo des villes du Maroc", layout="wide")

df = load_weather_data()

st.title("Bulletin météo des villes du Maroc")

if df.empty:
    st.warning("Aucune donnée disponible. Lancez la pipeline weather_pipeline pour charger les prévisions.")
    st.stop()

dates = sorted(df["date"].unique())
anchor = date.today() if date.today() in dates else dates[0]
idx = dates.index(anchor)
tomorrow = dates[idx + 1] if idx + 1 < len(dates) else anchor

c1, c2, c3, c4, c5 = st.columns(5)

nb_villes = df["city"].nunique()
nb_periodes_risque = int((df["risk_score"] >= RISK_THRESHOLD).sum())

row_temp_max = df.loc[df["temperature_2m_max"].idxmax()]
row_precip_max = df.loc[df["precipitation_sum"].idxmax()]
row_risk_max = df.loc[df["risk_score"].idxmax()]

c1.metric("Nombre de villes", f"{nb_villes}")

c2.metric("Température maximale", f"{row_temp_max['temperature_2m_max']:.1f} °C")
c2.caption(f"Ville : {row_temp_max['city']}")

c3.metric("Précipitations maximales", f"{row_precip_max['precipitation_sum']:.1f} mm")
c3.caption(f"Ville : {row_precip_max['city']}")

c4.metric("Périodes à risque", f"{nb_periodes_risque}")

c5.metric("Risque le plus élevé", row_risk_max["city"])
c5.caption(f"Score de risque : {int(row_risk_max['risk_score'])}")

st.divider()

st.subheader("Villes les plus à risque")
col_today, col_tomorrow = st.columns(2)

today_df = df[df["date"] == anchor].sort_values("risk_score", ascending=False)
tomorrow_df = df[df["date"] == tomorrow].sort_values("risk_score", ascending=False)

RISK_COLUMNS = ["city", "temperature_2m_max", "temperature_2m_min",
                "precipitation_sum", "risk_score"]

with col_today:
    st.markdown(f"**Aujourd'hui ({anchor})**")
    st.dataframe(today_df[RISK_COLUMNS].head(10), width="stretch", hide_index=True)
    chart = today_df.set_index("city")["risk_score"].head(15)
    if chart.notna().any():
        st.bar_chart(chart)

with col_tomorrow:
    st.markdown(f"**Demain ({tomorrow})**")
    st.dataframe(tomorrow_df[RISK_COLUMNS].head(10), width="stretch", hide_index=True)
    chart = tomorrow_df.set_index("city")["risk_score"].head(15)
    if chart.notna().any():
        st.bar_chart(chart)

st.divider()

st.subheader(f"Températures maximales par ville ({anchor})")
temp_chart = today_df.sort_values("temperature_2m_max", ascending=False).set_index("city")["temperature_2m_max"]
st.bar_chart(temp_chart)

st.subheader(f"Précipitations par ville ({anchor})")
precip_chart = today_df.sort_values("precipitation_sum", ascending=False).set_index("city")["precipitation_sum"]
st.bar_chart(precip_chart)

st.divider()

st.subheader("Aperçu des données")
st.dataframe(
    df.sort_values(["date", "risk_score"], ascending=[True, False]).head(20),
    width="stretch",
    hide_index=True,
)