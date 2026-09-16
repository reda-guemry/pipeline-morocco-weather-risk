import pandas as pd 

def risk_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the risk score based on weather conditions.
    """
    if data is None:
        print("Failed to load data.")
        return None

    def calculate_risk(row):
        score = 0
        if row['temperature_category'] in ['Hot', 'Very Hot']:
            score += 20
        elif row['temperature_category'] == 'Warm':
            score += 10

        if row['precipitation_category'] in ['Heavy Rain', 'Very Heavy Rain']:
            score += 20
        elif row['precipitation_category'] == 'Moderate Rain':
            score += 10

        if row['wind_speed_category'] in ['Strong Wind', 'Very Strong Wind']:
            score += 20
        elif row['wind_speed_category'] == 'Moderate Wind':
            score += 10

        return score

    data['risk_score'] = data.apply(calculate_risk, axis=1)
    return data