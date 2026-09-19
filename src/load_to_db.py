"""
Airflow-safe database loader.

Replaces the ORM-based loader (src/database/loader.py) for use inside Airflow 3.0.6,
which pins sqlalchemy<2.0 while the project models require sqlalchemy>=2.0.
This module builds no ORM models - it uses psycopg2 directly, so it imports cleanly
inside the stock apache/airflow image (psycopg2 ships with it).

Schema targets (created by alembic):
  cities(id, name, timezone, latitude, longitude, country)          UNIQUE(name)
  weather_forecasts(id, city_id FK, date, temperature_2m_max, ... ) UNIQUE(city_id, date)
"""

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from src.config import DATA_GOLD_PATH

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CITIES_COLUMNS = ['city', 'timezone', 'lat', 'lng', 'country']
WEATHER_COLUMNS = [
    'time', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum',
    'precipitation_probability_max', 'windspeed_10m_max', 'windgusts_10m_max',
    'weathercode', 'temperature_category', 'precipitation_category',
    'wind_speed_category', 'is_rainy', 'risk_score',
]


def _conn():
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'postgres'),
        port=os.getenv('DATABASE_PORT'),
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
    )


def _as_bool(value) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('true', '1', 'yes')


def _as_int(value) -> int:
    return int(float(value)) if value is not None and value == value else 0


def _upsert_cities(conn, df) -> dict:
    """Insert or update cities, return {city_name: city_id}."""
    cities = (
        df[CITIES_COLUMNS]
        .drop_duplicates('city')
        .to_dict('records')
    )

    id_by_name = {}
    with conn.cursor() as cur:
        insert = """
            INSERT INTO cities (name, timezone, latitude, longitude, country)
            VALUES (%(name)s, %(timezone)s, %(latitude)s, %(longitude)s, %(country)s)
            ON CONFLICT (name) DO UPDATE SET
                timezone = EXCLUDED.timezone,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                country = EXCLUDED.country
            RETURNING id, name
        """
        for city in cities:
            cur.execute(insert, {
                'name': city['city'],
                'timezone': city['timezone'],
                'latitude': city['lat'],
                'longitude': city['lng'],
                'country': city['country'],
            })
            new_id, name = cur.fetchone()
            id_by_name[name] = new_id

    return id_by_name


def _upsert_weather(conn, df, id_by_name) -> int:
    """Insert or update weather forecasts, return total rows written."""
    rows = []
    for _, row in df.iterrows():
        city_id = id_by_name.get(row['city'])
        if city_id is None:
            continue

        rows.append((
            city_id,
            pd.to_datetime(row['time']).date(),
            float(row['temperature_2m_max']),
            float(row['temperature_2m_min']),
            _as_int(row['precipitation_sum']),
            _as_int(row['precipitation_probability_max']),
            float(row['windspeed_10m_max']),
            float(row['windgusts_10m_max']),
            _as_int(row['weathercode']),
            row.get('temperature_category'),
            row.get('precipitation_category'),
            row.get('wind_speed_category'),
            _as_bool(row.get('is_rainy')),
            _as_int(row.get('risk_score')),
        ))

    if not rows:
        return 0

    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO weather_forecasts (
                city_id, date, temperature_2m_max, temperature_2m_min,
                precipitation_sum, precipitation_probability_max,
                windspeed_10m_max, windgusts_10m_max, weathercode,
                temperature_category, precipitation_category,
                wind_speed_category, is_rainy, risk_score
            ) VALUES %s
            ON CONFLICT (city_id, date) DO UPDATE SET
                temperature_2m_max = EXCLUDED.temperature_2m_max,
                temperature_2m_min = EXCLUDED.temperature_2m_min,
                precipitation_sum = EXCLUDED.precipitation_sum,
                precipitation_probability_max = EXCLUDED.precipitation_probability_max,
                windspeed_10m_max = EXCLUDED.windspeed_10m_max,
                windgusts_10m_max = EXCLUDED.windgusts_10m_max,
                weathercode = EXCLUDED.weathercode,
                temperature_category = EXCLUDED.temperature_category,
                precipitation_category = EXCLUDED.precipitation_category,
                wind_speed_category = EXCLUDED.wind_speed_category,
                is_rainy = EXCLUDED.is_rainy,
                risk_score = EXCLUDED.risk_score
            """,
            rows,
        )

    return len(rows)


def run_loader_pipeline() -> dict:
    """Load data/gold/final_data.csv into the `wheater` postgres database."""
    gold_path = PROJECT_ROOT / DATA_GOLD_PATH
    if not gold_path.exists():
        raise FileNotFoundError(f"Gold data not found at {gold_path}")

    df = pd.read_csv(gold_path)

    conn = _conn()
    try:
        id_by_name = _upsert_cities(conn, df)
        weather_written = _upsert_weather(conn, df, id_by_name)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    summary = {
        'cities': len(id_by_name),
        'weather_rows': weather_written,
        'source': str(gold_path),
    }
    print(f"[load_to_db] Loaded {summary['cities']} cities and "
          f"{summary['weather_rows']} weather forecasts.")
    return summary