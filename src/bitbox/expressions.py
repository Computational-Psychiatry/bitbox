from .utilities import get_data_values
from .signal_processing import peak_detection, outlier_detectionIQR
from .utilities import landmark_to_feature_mapper
import numpy as np
import pandas as pd

# Calculate asymmetry scores using mirror error approach
def asymmetry(landmarks):
    # read actual values
    data = get_data_values(landmarks)
    # TODO: check if data is dictionary and have the right keys
    # if not user should supply them as parameters
    dimension = landmarks['dimension']
    schema = landmarks['schema']
    
    rel_ids = landmark_to_feature_mapper(schema=schema)
    rel_ids_mirrored = landmark_to_feature_mapper(schema=schema+'_mirrored')
    
    feature_idx = {
        'eye': rel_ids['le'],
        'brow': rel_ids['lb'],
        'nose': rel_ids['no'],
        'mouth': np.concatenate((rel_ids['ul'], rel_ids['ll']))
    }
    feature_idx_mirrored = {
        'eye': rel_ids_mirrored['le'],
        'brow': rel_ids_mirrored['lb'],
        'nose': rel_ids_mirrored['no'],
        'mouth': np.concatenate((rel_ids_mirrored['ul'], rel_ids_mirrored['ll']))
    }

    mirror_mx = np.eye(3)
    mirror_mx[0,0] = -1
    
    T = data.shape[0]
    
    # for each frame, compute asymmetry scores for each feature
    asymmetry_scores = np.full((T, 5), np.nan)
    for t in range(T):
        coords = data[t, :]
        
        if len(coords) % dimension != 0:
            raise ValueError(f"Landmarks are not {dimension} dimensional. Please set the correct dimension.")
        
        num_landmarks = int(len(coords) / dimension)
        coords = coords.reshape((num_landmarks, dimension))

        # Compute mirrored error for each feature
        for i, feat in enumerate(feature_idx.keys()):
            x = coords[feature_idx[feat], :]
            y = coords[feature_idx_mirrored[feat], :]@mirror_mx
            
            score = np.mean(np.sqrt(np.sum((x-y)**2, axis=1)))
            asymmetry_scores[t, i] = score
        asymmetry_scores[t, 4] = np.mean(asymmetry_scores[t, 0:4])
    
    column_names = list(feature_idx.keys())+['overall']
    asymmetry_scores = pd.DataFrame(data=asymmetry_scores, columns=column_names)
             
    return asymmetry_scores


# use_negatives: whether to use negative peaks, 0: only positive peaks, 1: only negative peaks, 2: both
def expressivity(activations, axis=0, use_negatives=0, num_scales=6, robust=True, fps=30):
    # make sure data is in the right format
    data = get_data_values(activations)
    
    # whether rows are time points (axis=0) or signals (axis=1)
    if axis == 1:
        data = data.T
    
    num_signals = data.shape[1]
    
    expresivity_stats = []
    # define dataframes for each scale
    for s in range(num_scales):
         # number of peaks, density (average across entire signal), mean (across peak activations), std, min, max
        _data = pd.DataFrame(columns=['number', 'density', 'mean', 'std', 'min', 'max'])
        expresivity_stats.append(_data)
    
    # for each signal
    for i in range(num_signals):
        signal = data[:,i]
        
        # detect peaks at multiple scales
        peaks = peak_detection(signal, num_scales=num_scales, fps=fps, smooth=True, noise_removal=False)
        
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
            # if robust, we only consider inliers (removing outliers)
            peaked_signal = signal[idx]
            if robust and len(idx) > 5:
                outliers = outlier_detectionIQR(peaked_signal)
                peaked_signal = np.delete(peaked_signal, outliers)
                
            # calculate the statistics
            if len(peaked_signal) == 0:
                print("No peaks detected for signal %d at scale %d" % (i, s))
                results = np.zeros(6)
            else:
                _number = len(peaked_signal)
                _average = peaked_signal.sum() / len(signal)
                _mean = peaked_signal.mean()
                _std = peaked_signal.std()
                _min = peaked_signal.min()
                _max = peaked_signal.max()
                results = [_number, _average, _mean, _std, _min, _max]
        
            expresivity_stats[s].loc[i] = results
        
    return expresivity_stats


def diversity(landmarks):
    print("Calculating diversity")
    
