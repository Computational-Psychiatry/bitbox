import numpy as np
from scipy.ndimage import gaussian_filter

def peak_detection(data, smooting=True, smoothing_std=1, enhance=True):
    # check if the data is a list
    if not isinstance(data, list):
        datal = [data]
    else:
        datal = data
        
    # for each signal in the list    
    for i in range(len(datal)):
        signal = datal[i]
        
        # apply smoothing to remove noise
        if smooting:
            signal = gaussian_filter(signal, sigma=smoothing_std)
            
        # enhance the peaks
        dog_signal = signal - gaussian_filter(signal, sigma=smoothing_std*2)

        
        # peak detection. Treat positive and negative peaks separately
        # output is 0,1, or -1, with 1 for positive peaks and -1 for negative peaks
        positives = signal.copy()
        negatives = signal.copy()
        positives[positives < 0] = 0
        negatives[negatives > 0] = 0
        _data = [positives, negatives]
        peaked = np.zeros_like(signal)
        for s in range(2):
            _d = np.abs(_data[s])
            jumps = np.diff(np.sign(np.diff(_d)))
            peaks = np.where(jumps == -2)[0] + 1
            peaked[peaks] = 1 if s == 0 else -1
        datal[i] = signal * peaked
            
    if not isinstance(data, list):
        datal = datal[0]
        
    return data
    
    
    
    
    
    
    
    
    
    
    
    # # smoothing
    # for subject in range((len(frame_starts)-1)):
    #     start = frame_starts[subject]
    #     stop = frame_starts[(subject+1)]
    #     all_tseries[start:stop, :] = ndimage.gaussian_filter(all_tseries[start:stop, :], sigma=[smoothing_std, 0])
        
    # #peak detection
    # positives = all_tseries.copy()
    # negatives = all_tseries.copy()
    # positives[positives<0] = 0
    # negatives[negatives>0] = 0
    # _data = [positives, negatives]
    # peaked = np.zeros_like(all_tseries)
    # for s in range(2):
    #     _d = np.abs(_data[s])
    #     jumps = np.diff(np.sign(np.diff(_d, axis=0)),axis=0)
    #     peaks = np.where(jumps==-2)
    #     peaks = (peaks[0]+1, peaks[1])
    #     peaked[peaks] = 1
        
    # all_tseries = all_tseries * peaked
        
    # return all_tseries