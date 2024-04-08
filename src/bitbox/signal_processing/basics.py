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


def outlier_detection(data, thresh=3.5):
    # compute median-absolute-deviation (MAD)
    median = np.median(data)
    diff = np.sqrt((data-median)**2)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation

    # remove outliers
    trimmed_data = data[modified_z_score < thresh]
    
    # Return the trimmed data
    return trimmed_data