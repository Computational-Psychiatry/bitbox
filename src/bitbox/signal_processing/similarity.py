from scipy.stats import pearsonr, spearmanr
import math
import numpy as np

def _xcorr(x, y, ordinal=False):   
    if ordinal:
        correlation = spearmanr
    else:
        correlation = pearsonr
    
    # pick the shorter array and slide in the longer one
    if len(x) <= len(y):
        width = len(x)
        shorter = x
        longer = y
    else:
        width = len(y)
        shorter = y
        longer = x
        
    rs = []
    for n in range(0, len(longer) - width):
        # get chunk (of size width) of the longer array 
        chunk = longer[n:n+width]
        
        # correlate whole shorter with the chunk of the longer
        r = correlation(shorter, chunk)[0]
        if math.isnan(r):
            r = 0.0
            
        rs.append(r)
    
    return rs


def windowed_cross_correlation_2S(x, y, width=0.5, lag=None, step=None, fps=30, ordinal=False, negative=0):
    width = int(round(fps*width))
    
    if step is None:
        step = int(width/2.)
    else:
        step = int(round(fps*step))
    
    if lag is None:
        lag = int(width/4.)
    else:
        lag = int(round(fps*lag))
    
    # pick the shorter array and slide in the longer one
    if len(x) <= len(y):
        length = len(x)
        shorter = x
        longer = y
    else:
        length = len(y)
        shorter = y
        longer = x

    corrs = []
    for n in range(0, length-width, step):
        # get a window within the shorter array
        baseline = shorter[n:(n+width)]
        
        # get an extended window within the longer array
        start = max(0, n-lag)
        stop = min(len(longer), n+width+lag)
        query = longer[start:stop]
        
        # calculate all possible lagged xcorrs
        cor = _xcorr(baseline, query, ordinal=ordinal)
        
        # get the maximum xcorr
        # there are three options when treating negative values
        # 0: [Default] take the maximum value regardless of the sign
        # 1: take the maximum absolute value
        # 2: take the maximum positive value, which will be probably the same as 0
        if negative==0:
            m = np.max(cor)
        elif negative==1:
            idx = np.argmax(np.abs(cor))
            m = cor[idx]
        else:
            cor = np.array(cor)
            cor[cor<0] = 0
            m = np.max(cor)
        corrs.append(m)
    
    return np.array(corrs)


def windowed_cross_correlation(X, Y, width=0.5, lag=None, step=None, fps=30):
    width = int(round(fps*width))
    
    if step is None:
        step = int(width/2.)
    else:
        step = int(round(fps*step))
    
    if lag is None:
        lag = int(width/4.)
    else:
        lag = int(round(fps*lag))
    
    T = min((X.shape[0], Y.shape[0]))
    
    pairs = [(i1, i2) for i1 in range(0,X.shape[1]) for i2 in range(0,Y.shape[1])]
    
    window_offsets = range(0, T-width, step)
    Nwindows = len(window_offsets)
    Xcorr = np.zeros((Nwindows, len(pairs)))
    Xlag  = np.zeros((Nwindows, len(pairs)))
    
    pidx = 0
    for pidx in range(0, len(pairs)):
        pair = pairs[pidx]
        
        if pair[0] == pair[1]:
            continue
        
        for tidx in range(0, Nwindows):
            t1 = window_offsets[tidx]
            t2 = t1
            
            x = X[range(t1,t1+width), pair[0]]
            y = Y[range(t2,t2+width), pair[1]]
        
            nx = (x-np.mean(x))/(np.std(x)*len(x)+np.finfo(float).eps)
            ny = (y-np.mean(y))/(np.std(y)+np.finfo(float).eps)
        
            corr = np.correlate(nx, ny, 'full')
        
            zero_out_frames = round((width - lag))
            corr[0:zero_out_frames] = -1
            corr[0:round(len(corr)/2.0)] = -1
            corr[-zero_out_frames:] = -1
                                
            maxcorr = np.max(corr)
            maxlag = (np.argmax(corr) - round(width / 2)) / fps # in seconds
        
            Xcorr[tidx, pidx] = maxcorr
            Xlag[tidx, pidx] = maxlag
            
    return Xcorr, Xlag
