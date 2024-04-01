from .signal_processing import windowed_cross_correlation
from .utilities import dictionary_to_array

import numpy as np

def intra_person_coordination(data, axis=0, width=90, lag=None, step=None, ordinal=False):
    # check if data is a dictionary
    if isinstance(data, dict):
        data = dictionary_to_array(data)
    
    # whether rows are time points (axis=0) or signals (axis=1)
    if axis == 1:
        data = data.T
        
    num_signals = data.shape[1]
    
    corr_mean = np.zeros((num_signals, num_signals))
    corr_std = np.zeros((num_signals, num_signals))
    
    # for each pair of signals
    for i in range(num_signals-1):
        for j in range(i+1, num_signals):
            x = data[:,i]
            y = data[:,j]
            
            # calculate the windowed cross-correlation
            corrs = windowed_cross_correlation(x, y, width=width, lag=lag, step=step, ordinal=ordinal)
            
            # calculate the average correlation
            corr_mean[i,j] = corr_mean[j,i] = np.mean(corrs)
            corr_std[i,j] = corr_std[j,i] = np.std(corrs)
            
    return corr_mean, corr_std


            
            