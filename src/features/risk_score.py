import numpy as np
import pandas as pd


def risk_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a 0-100 daily risk score from the weather conditions.

    Simple rule: each hazard adds points based on a few fixed thresholds.

      Temperature (max):
          > 40C  -> +40     > 35C -> +25     > 30C -> +10
      Rain (accumulated):
          > 20mm -> +35     > 8mm -> +20     > 2mm -> +10     > 0mm -> +5
      Wind (peak, gusts counted at 60%):
          > 50 km/h -> +25  > 30 km/h -> +10

    Score (0 to 100) = heat + rain + wind points.
    """
    if data is None:
        print("Failed to load data.")
        return None

    temp = np.nan_to_num(data["temperature_2m_max"].astype(float))
    rain = np.nan_to_num(data["precipitation_sum"].astype(float))
    wind = np.nan_to_num(data["windspeed_10m_max"].astype(float))
    gust = np.nan_to_num(data["windgusts_10m_max"].astype(float))
    peak_wind = np.maximum(wind, 0.6 * gust)

    heat = np.where(temp > 40, 40, np.where(temp > 35, 25, np.where(temp > 30, 10, 0)))
    rain_points = np.where(
        rain > 20, 35,
        np.where(rain > 8, 20, np.where(rain > 2, 10, np.where(rain > 0, 5, 0)))
    )
    wind_points = np.where(peak_wind > 50, 25, np.where(peak_wind > 30, 10, 0))

    data["risk_score"] = (heat + rain_points + wind_points).astype(int)
    return data