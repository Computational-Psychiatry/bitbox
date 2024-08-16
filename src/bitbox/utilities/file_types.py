import numpy as np
import pandas as pd

def get_data_values(data):
    # check if data is a dictionary
    if isinstance(data, dict):
        data = dictionary_to_array(data)
    
    return data


def dictionary_to_array(data):
    if isinstance(data, dict):
        if 'data' in data and isinstance(data['data'], pd.DataFrame):
            return data['data'].values
    
    raise ValueError("Unrecognized data type")