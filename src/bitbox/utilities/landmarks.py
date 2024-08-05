import numpy as np

def landmark_to_feature_mapper(schema='ibug51'):
    idx = {}
    
    if schema == 'ibug51':
        idx = {'lb': np.array(list(range(0, 5))),
               'rb': np.array(list(range(5, 10))),
               'no': np.array(list(range(10, 19))),
               'le': np.array(list(range(19, 25))),
               're': np.array(list(range(25, 31))),
               'ul': np.array(list(range(31, 37))+list(range(43, 47))),
               'll': np.array(list(range(37, 43))+list(range(47, 51)))}
    elif schema == 'ibug51_mirrored':
        idx = {'lb': np.array([9,8,7,6,5]),
               'rb': np.array([4,3,2,1,0]),
               'no': np.array([10, 11, 12, 13, 18, 17, 16, 15, 14]),
               'le': np.array([28, 27, 26, 25, 30, 29]),
               're': np.array([22, 21, 20, 19, 24, 23]),
               'ul': np.array([37, 36, 35, 34, 33, 32, 47, 46, 45, 44]),
               'll': np.array([31, 42, 41, 40, 39, 38, 43, 50, 49, 48])}
    else:
        raise ValueError(f"Landmark schema {schema} not recognized")
    
    return idx