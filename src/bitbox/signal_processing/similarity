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

def windowed_cross_correlation(x, y, width=90, lag=None, step=None, ordinal=False, negative=0):
    if step is None:
        step = int(width/2.)
    
    if lag is None:
        lag = int(width/4.)
    
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