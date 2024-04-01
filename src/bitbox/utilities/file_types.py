import numpy as np

def dictionary_to_array(data):
    if isinstance(data, dict):
        if 'data' in data and isinstance(data['data'], dict):
            frames = [f"frame{i}" for i in range(len(data['data']))]
            if all(frame in data['data'] for frame in frames):
                return np.array(list(data['data'].values()), dtype=float)
    
    raise ValueError("Unrecognized data type")