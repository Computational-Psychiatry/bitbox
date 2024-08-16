from .utilities import get_data_values
from .signal_processing import peak_detection, outlier_detectionIQR, log_transform
from .utilities import landmark_to_feature_mapper
import numpy as np
import pandas as pd

# Calculate asymmetry scores using mirror error approach
def asymmetry(landmarks, axis=0):
    # read actual values
    data = get_data_values(landmarks)
    
    # whether rows are time points (axis=0) or signals (axis=1)
    if axis == 1:
        data = data.T
    
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

    mirror_mx = np.eye(dimension)
    mirror_mx[0,0] = -1
    
    T = data.shape[0]
    
    # for each frame, compute asymmetry scores for each feature
    asymmetry_scores = np.full((T, len(feature_idx.keys())+1), np.nan)
    
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
        asymmetry_scores[t, -1] = np.mean(asymmetry_scores[t, 0:-1])
    
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
                _density = peaked_signal.sum() / len(signal)
                _mean = peaked_signal.mean()
                _std = peaked_signal.std()
                _min = peaked_signal.min()
                _max = peaked_signal.max()
                results = [_number, _density, _mean, _std, _min, _max]
        
            expresivity_stats[s].loc[i] = results
        
    return expresivity_stats


def diversity(activations, axis=0, use_negatives=0, num_scales=6, robust=True, fps=30):
    # make sure data is in the right format
    data = get_data_values(activations)
    
    # whether rows are time points (axis=0) or signals (axis=1)
    if axis == 1:
        data = data.T
        
    num_frames, num_signals = data.shape
    
    #STEP 1: Detect peaks at multiple scales
    #---------------------------------------

    # peak data will have shape (num_scales, num_frames, num_signals)
    # we will compute diversity for pos and neg separately and take the average
    data_peaked_pos = [0] * num_scales
    data_peaked_neg = [0] * num_scales
    for s in range(num_scales):
        data_peaked_pos[s] = np.zeros((num_frames, num_signals))
        data_peaked_neg[s] = np.zeros((num_frames, num_signals))

    for i in range(num_signals):
        signal = data[:, i]
        
        # detect peaks at multiple scales
        peaks = peak_detection(signal, num_scales=num_scales, fps=fps, smooth=True, noise_removal=False)
        
        for s in range(num_scales):
            _peaks = peaks[s, :]
            
            # whether we use negative peaks or not
            if use_negatives == 0: # only use positives
                _peaks[_peaks==-1] = 0
            elif use_negatives == 1: # only use negatives
                _peaks[_peaks==1] = 0
            
            # if robust, we only consider inliers (removing outliers)
            idx = np.where(_peaks!=0)[0]
            if robust and len(idx) > 5:
                outliers = outlier_detectionIQR(signal[idx])
                idx = np.delete(idx, outliers)
            tmp = _peaks[idx]
            _peaks[:] = 0
            _peaks[idx] = tmp
            
            # store the peaked signal
            signal_pos = np.zeros_like(signal)
            signal_pos[_peaks==1] = signal[_peaks==1]
            signal_neg = np.zeros_like(signal)
            signal_neg[_peaks==-1] = signal[_peaks==-1]
            
            data_peaked_pos[s][:, i] = signal_pos
            data_peaked_neg[s][:, i] = signal_neg
            
    #STEP 2: Compute diversity at each scale
    #---------------------------------------
    diversity = pd.DataFrame(index=range(num_scales), columns=['overall', 'frame_wise'])
    for s in range(num_scales):
        
        data_final = []
        if use_negatives == 0: # only use positives
            data_final = [data_peaked_pos[s]]
        elif use_negatives == 1: # only use negatives
            data_final = [data_peaked_neg[s]]
        elif use_negatives == 2: # use both
            data_final = [data_peaked_pos[s], data_peaked_neg[s]]
        else:
            raise ValueError("Invalid value for use_negatives")
        
        # compute entropy for pos and neg separately and take the average
        entropy = 0
        entropy_frame = 0
        for data_peaked in data_final:            
            #TODO: make sure each signal has the same range. Otherwise, we need to normalize the probabilities
            
            base = num_signals#2
            
            # type 1: compute for the entire time period
            prob = np.abs(data_peaked).sum(axis=0)
            normalizer = prob.sum()
            if normalizer > 0:
                prob /= normalizer
            
            log_prob = log_transform(prob, base)
            
            # type 2: compute for each frame separately and take the average
            prob_frame = np.zeros_like(data_peaked)
            for f in range(num_frames):
                normalizer = np.abs(data_peaked[f, :]).sum()
                if normalizer > 0:
                    prob_frame[f, :] = np.abs(data_peaked[f, :]) / normalizer
            prob_frame[np.isinf(prob_frame)] = 0
            prob_frame[np.isnan(prob_frame)] = 0
            
            log_prob_frame = log_transform(prob_frame, base)
            
            entropy += -1 * np.sum(prob * log_prob)
            entropy_frame += -1 * np.sum(prob_frame * log_prob_frame, axis=1)
            
        entropy /= len(data_final)
        entropy_frame /= len(data_final)
        
        diversity.loc[s, :] = [entropy, entropy_frame.mean()]
    
    return diversity
            
