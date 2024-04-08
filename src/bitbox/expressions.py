from .utilities import dictionary_to_array
from .signal_processing import peak_detection

import numpy as np

def _data_within_95_percent(data):
    # Sort the data
    sorted_data = np.sort(data)
    
    # Calculate the indices for the 2.5th and 97.5th percentiles
    low_index = int(np.ceil(len(sorted_data) * 0.025))
    high_index = int(np.floor(len(sorted_data) * 0.975))
    
    # Extract the middle 95% of the data
    trimmed_data = sorted_data[low_index:high_index]
    
    # Return the trimmed data
    return trimmed_data


def _outlier_detection(data, thresh=3.5):
    # compute median-absolute-deviation (MAD)
    median = np.median(data)
    diff = np.sqrt((data-median)**2)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation

    # remove outliers
    trimmed_data = data[modified_z_score < thresh]
    
    # Return the trimmed data
    return trimmed_data


def symmetry(landmarks):
    print("Calculating symmetry")


# use_negatives: whether to use negative peaks, 0: only positive peaks, 1: only negative peaks, 2: both
def expressivity(data, axis=0, use_negatives=0, num_scales=6, robust=True, fps=30):
    # check if data is a dictionary
    if isinstance(data, dict):
        data = dictionary_to_array(data)
    
    # whether rows are time points (axis=0) or signals (axis=1)
    if axis == 1:
        data = data.T
    
    num_signals = data.shape[1]
    
    expresivity_stats = []
    
    # for each signal
    for i in range(num_signals):
        signal = data[:,i]
        
        # detect peaks at multiple scales
        peaks = peak_detection(signal, num_scales=num_scales, fps=fps, smooth=True, noise_removal=False)
        
        # number of peaks, overall average (across entire signal), mean (across peak activations), std, min, max
        results = np.zeros([num_scales, 6])
        
        for s in range(num_scales):
            _peaks = peaks[s, :]
            
            # whether we use negative peaks
            if use_negatives == 0:
                idx = np.where(_peaks==1)[0]
            elif use_negatives == 1:
                idx = np.where(_peaks==-1)[0]
            elif use_negatives == 2:
                idx = np.where(_peaks!=0)[0]
            else:
                raise ValueError("Invalid value for use_negatives")
            
            # extract the peaked signal
            # if robust, we only consider the 95% of the data, removing possible outliers and noise
            if robust and len(idx) > 10:
                peaked_signal = _outlier_detection(signal[idx])
            else:
                peaked_signal = signal[idx]
            
            # calculate the statistics
            if len(peaked_signal) == 0:
                print("No peaks detected for signal %d at scale %d" % (i, s))
                results[s, :] = [0, 0, 0, 0, 0, 0]
            else:
                _number = len(peaked_signal)
                _average = peaked_signal.sum() / len(signal)
                _mean = peaked_signal.mean()
                _std = peaked_signal.std()
                _min = peaked_signal.min()
                _max = peaked_signal.max()
                results[s, :] = [_number, _average, _mean, _std, _min, _max]
        
        expresivity_stats.append(results)
        
    return expresivity_stats


def diversity(landmarks):
    print("Calculating diversity")