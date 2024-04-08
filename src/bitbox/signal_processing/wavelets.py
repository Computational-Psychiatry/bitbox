import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pylab as plt

import pywt

def _value_at_percentile(data, percentile):
    # Sort the data
    sorted_data = np.sort(data)
    # Calculate the index. Note: numpy uses 0-based indexing
    index = int(np.floor(len(sorted_data) * percentile / 100.0))
    # Ensure the index is within the bounds of the list
    index = min(max(index, 0), len(sorted_data) - 1)
    # Return the value at the calculated index
    return sorted_data[index]

def _peak_detector(signal, noise_removal=False):
    # Treat positive and negative peaks separately
    # output is 0,1, or -1, with 1 for peaks and -1 for valleys
    positives = signal.copy()
    negatives = signal.copy()
    positives[positives < 0] = 0
    negatives[negatives > 0] = 0
    
    _data = [positives, negatives]
    output = np.zeros_like(signal)
    
    for s in range(2):
        # detect all peaks/valleys where derivative changes sign
        _d = np.abs(_data[s])
        jumps = np.diff(np.sign(np.diff(_d)))
        peaks = np.where(jumps == -2)[0] + 1
        
        # remove tiny peaks
        if noise_removal:
            magnitudes = np.abs(signal[peaks])
            thresholds = _value_at_percentile(magnitudes, 97.5) * 0.1
            idx = np.where(magnitudes < thresholds)[0]
            peaks = np.delete(peaks, idx)
        
        output[peaks] = 1 if s == 0 else -1
        
    return output

def _wavelet_decomposition(signal, scales):
    # decomposition
    cwtmatr, freqs = pywt.cwt(signal, scales, 'mexh')
    
    # smooth coefficients
    cwtmatr = np.array([gaussian_filter(cwtmatr[s, :], sigma=1) for s in range(cwtmatr.shape[0])])
       
    return cwtmatr

def _visualize_peaks(signal, wavelets, peaks, fps):
    num_scales = wavelets.shape[0]
    dt = 1. / fps
    seconds = dt * np.arange(len(signal))
    
    fig, ax = plt.subplots(num_scales+1, 1, figsize=(25, num_scales*3))
    x = [signal] + [wavelets[s,:] for s in range(num_scales)]
    
    for s in range(num_scales+1):
        if s == 0:
            _peaks = peaks.sum(axis=0)
            _peaks[_peaks>0] = 1
            _peaks[_peaks<0] = -1
        else:
            _peaks = peaks[s-1, :]
            
        ax[s].plot(seconds, x[s])
        ax[s].hlines(x[s].mean(), xmin=seconds.min(), xmax=seconds.max(), ls='--')
        
        ax[s].vlines(seconds[np.where(_peaks==1)[0]], ymin=x[s].min(), ymax=x[s].max(), colors='blue', linewidth=1)
        ax[s].vlines(seconds[np.where(_peaks==-1)[0]], ymin=x[s].min(), ymax=x[s].max(), colors='red', linewidth=1)
        
        dx = round(seconds.max() / 40, 2)
        ax[s].set_xticks(np.arange(0, seconds.max()+dx, dx))

def peak_detection(data, num_scales=6, fps=30, smooth=True, noise_removal=False, visualize=False):
    # check if the data is a list
    if not isinstance(data, list):
        datal = [data]
    else:
        datal = data
        
    # for each signal in the list
    peaksl = []
    for i in range(len(datal)):
        signal_org = datal[i]
        
        # zero mean the signal
        signal = signal_org - signal_org.mean()
        
        # smooth the signal
        if smooth:
            signal = gaussian_filter(signal, sigma=1)
        
        # wavelet decomposition at multiple scales
        scales = (fps/30) * np.geomspace(1, 18, num=num_scales)      
        wavelets = _wavelet_decomposition(signal, scales)
        
        # peak detection at different scales
        peaks = np.zeros_like(wavelets)
        for s in range(num_scales):
            peaks[s, :] = _peak_detector(wavelets[s, :], noise_removal=noise_removal)
            
        peaksl.append(peaks)
            
        if visualize:
            _visualize_peaks(signal_org, wavelets, peaks, fps)
            
    if not isinstance(data, list):
        peaksl = peaksl[0]
    
    return peaksl