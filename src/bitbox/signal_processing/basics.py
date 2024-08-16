import numpy as np

def data_within_95_percent(data):
    # Sort the data
    sorted_data = np.sort(data)
    
    # Calculate the indices for the 2.5th and 97.5th percentiles
    low_index = int(np.ceil(len(sorted_data) * 0.025))
    high_index = int(np.floor(len(sorted_data) * 0.975))
    
    # Extract the middle 95% of the data
    trimmed_data = sorted_data[low_index:high_index]
    
    # Return the trimmed data
    return trimmed_data


def outlier_detectionMAD(data, thresh=3.5):
    # compute median-absolute-deviation (MAD)
    median = np.median(data)
    diff = np.sqrt((data-median)**2)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation

    # identify outliers
    outliers = np.where(modified_z_score > thresh)[0]
    
    return outliers


def outlier_detectionIQR(data):
    # 25 and 75 quartiles
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    
    # interquartile range
    IQR = Q3 - Q1
    
    # define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # identify outliers
    outliers = np.where((data < lower_bound) | (data > upper_bound))[0]
    
    return outliers

def log_transform(prob, base=2):
    log_prob = np.zeros_like(prob)
    log_prob[prob>0] = np.log(prob[prob>0]) / np.log(base) 
    log_prob[np.isinf(log_prob)] = 0
    log_prob[np.isnan(log_prob)] = 0
    
    return log_prob