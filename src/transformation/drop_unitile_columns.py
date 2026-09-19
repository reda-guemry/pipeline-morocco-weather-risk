import pandas as pd

def drop_unitile_columns(dataframe : pd.DataFrame) -> pd.DataFrame : 
    """
    Drop the meta columns from the DataFrame.
    """
    return dataframe.drop(columns=['longitude' , 'latitude' , 'iso2', 'capital' , '_merge' , 'admin_name'])

