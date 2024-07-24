from .utilities import dictionary_to_array
from .signal_processing import peak_detection, outlier_detectionIQR
from .utilities import mapperLandmarksToCordinatesEDMA, mapperLandmarksToCordinatesMirrorError, mouth_ul_ll_to_rm_lm
from scipy.spatial.distance import cdist
import math
import numpy as np
import pandas as pd

def _compute_edma_scores(**kwargs):
    """
    Calculate the asymmetry score using Euclidean distance matrix based approach.

    Args:
        **kwargs: Keyword arguments containing the left_region and right_region.

    Returns:
        float: The asymmetry score.

    Raises:
        KeyError: If the left_region or right_region is not provided in the kwargs.

    """
    # Check if left_region and right_region are provided in kwargs
    if "left_region" not in kwargs or "right_region" not in kwargs:
        raise KeyError("left_region and right_region must be provided in kwargs")

    # Extract the left and right regions from kwargs
    left_region = kwargs["left_region"]
    right_region = kwargs["right_region"]

    # Calculate the distance matrices for the left and right regions
    distance_matrix_left_region = cdist(left_region, left_region, 'sqeuclidean')
    distance_matrix_right_region = cdist(right_region, right_region, 'sqeuclidean')
    # Calculate the asymmetry score
    if (math.sqrt(np.mean(distance_matrix_left_region))) >= (math.sqrt(np.mean(distance_matrix_right_region))):
        asymmetry_score_region = (math.sqrt(np.mean(distance_matrix_left_region))) - (
                math.sqrt(np.mean(distance_matrix_right_region)))
    else:
        asymmetry_score_region = (math.sqrt(np.mean(distance_matrix_right_region))) - (
                math.sqrt(np.mean(distance_matrix_left_region)))

    return asymmetry_score_region


def _compute_mirror_error(region_wise_mapped_cordinates, region_wise_mapped_cordinates_reverse, region): 
    """
    Calculate the mirror error for each facial region.

    Args:
        region_wise_mapped_cordinates (dict): A dictionary containing the mapped coordinates for each facial region.
        region_wise_mapped_cordinates_reverse (dict): A dictionary containing the reverse mapped coordinates for each facial region.
        region (list): A list of facial regions.

    Returns:
        dict: A dictionary containing the mirror error scores for each facial region.

    """
    mirror_error_eye_brow = {}
    mirror_error_eye_region = {}
    mirror_error_mouth_region = {}
    mirror_error_overall = {}
    for frame_id,_ in zip(region_wise_mapped_cordinates, region_wise_mapped_cordinates_reverse):
        mirror_error_per_frame = {}
        for reg in region:
            # Calculate the mirror error for each region
            mirror_error_per_frame[reg] = np.mean(
                np.linalg.norm(np.matrix(region_wise_mapped_cordinates_reverse[frame_id][reg]) - np.matrix(
                  region_wise_mapped_cordinates[frame_id][reg]),ord=2,axis=1))
        mirror_error_overall[frame_id] = mirror_error_per_frame["lb"] + mirror_error_per_frame["rb"] + mirror_error_per_frame["re"] + mirror_error_per_frame["le"] + mirror_error_per_frame["mo"]  #mirror_error_per_frame["ll"]  + mirror_error_per_frame["ul"]    
        mirror_error_eye_brow[frame_id] = mirror_error_per_frame["lb"] + mirror_error_per_frame["rb"]
        mirror_error_eye_region[frame_id] = mirror_error_per_frame["re"] + mirror_error_per_frame["le"]
        mirror_error_mouth_region[frame_id] = mirror_error_per_frame["mo"]
    return mirror_error_eye_brow,mirror_error_eye_region,mirror_error_mouth_region,mirror_error_overall


def symmetryEDMA(landmarks, frames):
    """
    Calculate the symmetry scores for different facial regions based on landmark coordinates.

    Args:
        landmarks (dict): A dictionary containing the landmark coordinates for different facial regions.

    Returns:
        None

    """
    # Map landmarks to region-wise coordinates
    region_wise_mapped_cordinates = mapperLandmarksToCordinatesEDMA(landmarks,frames)

    # Calculate asymmetry scores for each facial region
    eyebrow_region_scores = {}
    eye_region_scores = {}
    mouth_region_scores = {}
    

    for frame in region_wise_mapped_cordinates:
        # Calculate asymmetry score for eyebrow region
        asymmetry_score_region_brow = _compute_edma_scores(left_region=region_wise_mapped_cordinates[frame]["lb"],
                                                  right_region=region_wise_mapped_cordinates[frame]["rb"])
        #eyebrow_region_scores[frame] = asymmetry_score_region_brow - 1
        eyebrow_region_scores[frame] = asymmetry_score_region_brow 

        # Calculate asymmetry score for eye region
        asymmetry_score_region_eye = _compute_edma_scores(left_region=region_wise_mapped_cordinates[frame]["le"],
                                                 right_region=region_wise_mapped_cordinates[frame]["re"])
        #eye_region_scores[frame] = asymmetry_score_region_eye - 1
        eye_region_scores[frame] = asymmetry_score_region_eye 

        # Calculate asymmetry score for mouth region
        lef_region_mouth, right_region_mouth = mouth_ul_ll_to_rm_lm(region_wise_mapped_cordinates[frame]["mo"])
        asymmetry_score_region_mouth = _compute_edma_scores(left_region=lef_region_mouth, right_region=right_region_mouth)
        #mouth_region_scores[frame] = asymmetry_score_region_mouth - 1
        mouth_region_scores[frame] = asymmetry_score_region_mouth 

    # Return the calculated asymmetry scores
    dict_outcomes_edma = {
        "eye_region_edma_scores": np.mean(list(eye_region_scores.values())),
        "eyebrow_region_edma_scores": np.mean(list(eyebrow_region_scores.values())),
        "mouth_region_edma_scores": np.mean(list(mouth_region_scores.values())),
        "overall_edma_scores": np.mean(list(eye_region_scores.values())) + np.mean(
            list(eyebrow_region_scores.values())) + np.mean(list(mouth_region_scores.values()))
    }    
    return dict_outcomes_edma

    

# Calculate symmetry scores using mirror error approach
def symmetryMirrorError(Landmarks, frames):
    """
    Calculate the symmetry scores for different facial regions based on landmark coordinates using the mirror error approach.

    Args:
        Landmarks (dict): A dictionary containing the landmark coordinates for different facial regions.

    Returns:
        dict: A dictionary containing the symmetry scores for each facial region.

    """
    # Map landmarks to region-wise coordinates using mirror error approach
    region_wise_mapped_cordinates, region_wise_mapped_cordinates_reverse, region = mapperLandmarksToCordinatesMirrorError(
        Landmarks,frames)
    
    # Calculate mirror error scores for each facial region
    mirror_error_eye_brow, mirror_error_eye_region, mirror_error_mouth_region, mirror_error_overall = _compute_mirror_error(region_wise_mapped_cordinates, region_wise_mapped_cordinates_reverse,
                                            region)
    # Return the calculated mirror error scores
    
    dict_outcomes_mirror_error = {
        "eye_region_mirror_error_scores": np.mean(list(mirror_error_eye_brow.values())),
        "eyebrow_region_mirror_error_scores": np.mean(list(mirror_error_eye_region.values())),
        "mouth_region_mirror_error_scores": np.mean(list(mirror_error_mouth_region.values())),
        "overall_mirror_error_scores": np.mean(list(mirror_error_overall.values()))
    }
    
    
    return dict_outcomes_mirror_error

def symmetry(landmarks, frames):
    """
    Calculate the symmetry scores for different facial regions based on landmark coordinates.

    Args:
        landmarks (dict): A dictionary containing the landmark coordinates for different facial regions.
        frames (list or None): A list of frame numbers to process scores for specific frame numbers. If None, all frames are processed.

    Returns:
        tuple: A tuple containing two dictionaries. The first dictionary contains the symmetry scores based on the EDMA approach, and the second dictionary contains the symmetry scores based on the mirror error approach.

    """
    print("Calculating symmetry")
    dict_scores_edma_asymmetry = symmetryEDMA(landmarks, frames)
    dict_scores_mirror_error_asymmetry = symmetryMirrorError(landmarks, frames)
    return dict_scores_edma_asymmetry, dict_scores_mirror_error_asymmetry


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
    
