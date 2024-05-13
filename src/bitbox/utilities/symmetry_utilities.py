import json
import os
import numpy as np

def landmarkFrameMapper(frame: str, landmarks: dict, landmark_regions: dict, region_mapping_coordinates_all_frames: dict, type: str) -> dict:
    """
    Maps landmarks to region-wise coordinates for a single frame.

    Parameters:
        frame (str): The frame identifier.
        landmarks (dict): The landmarks for the frame.
        landmark_regions (dict): The mapping of landmark regions.
        region_mapping_coordinates_all_frames (dict): The region mapping coordinates for all frames.
        type (str): The type of mapping to perform.

    Returns:
        dict: The updated region mapping coordinates for all frames.
    """

    # Create dictionary to store region mapping coordinates for the current frame
    region_mapping_coordinates_per_frame = {key: [] for key in list(landmark_regions.keys())}

    # Check if the number of landmarks is consistent
    if len(landmarks) != 51:
        raise ValueError("Inconsistencies are present. The landmarks should have a length of 51.")

    # Iterate over each region and landmark in the mapping
    for region, region_landmarks in landmark_regions.items():
        for landmark_id in list(region_landmarks):
            if type == "normal":
                # Convert landmarks to float values
                landmarksConverted = [(float(i)) for i in landmarks[landmark_id]]
                region_mapping_coordinates_per_frame[region].append(landmarksConverted)
            elif type == "reverse":
                # Convert landmarks to float values and flip along the x-axis
                landmarksConverted = [-(float(i)) if k == 0 else float(i) for k, i in enumerate(landmarks[landmark_id])]
                region_mapping_coordinates_per_frame[region].append(landmarksConverted)

        # Update the region mapping coordinates for the current frame
        region_mapping_coordinates_all_frames[frame] = region_mapping_coordinates_per_frame

    # Return the updated region mapping coordinates for all frames
    return region_mapping_coordinates_all_frames


def landmarkMappingRegionwiseCoordinates(data: dict, region_mapping: dict, frames:list, type="None") -> dict:
    """
    Maps landmarks to region-wise coordinates based on the provided region mapping.

    Parameters:
        data (dict): The input data containing landmarks.
        region_mapping (dict): The mapping of landmark regions.
        frames (list or None): The frames to process. If a list is provided, only the specified frames will be processed. If a None is provided, all frames will be processed.
        type (str): The type of mapping to perform. Options are "normal" and "reverse".

    Returns:
        dict: The region-wise coordinates for all frames.

    Raises:
        UserWarning: If an empty list is provided for frames, all frames will be processed by default.
        ValueError: If a negative frame id is provided or if frame id is not present within the video.

    """
    # Load landmark region mapping
    landmark_regions = {}

    if type == "normal":
        region_mapping = region_mapping["landmarkRegionMapping"]
    elif type == "reverse":
        region_mapping = region_mapping["landmarkRegionMappingReverse"]

    # Generate landmark regions for each region in the mapping
    for region in region_mapping:
        landmark_regions[region] = [f"l{x}" for x in region_mapping[region]]

    # Get all frames' landmarks
    allFramesLandmarks = data["data"]

    # Create dictionary to store region mapping coordinates for all frames
    region_mapping_coordinates_all_frames = {}

    # Check if frames is a list or a string
    if isinstance(frames, list):
        if len(frames) == 0:
            frames_list = []
            raise UserWarning("Provided an empty list with no specific frames. All frames will be processed by default.")
        else:
            if any(frame_id < 0 for frame_id in frames):
                raise ValueError("Frame id cannot be negative.")
            else:
                frames_list = [f"frame{x}" for x in frames]
    else:
        frames_list = list(allFramesLandmarks.keys())

    # Iterate over each frame's landmarks
    for frame in frames_list:
        try:
            # Get landmarks for current frame
            landmarks = allFramesLandmarks[frame]
            region_mapping_coordinates_all_frames = landmarkFrameMapper(frame, landmarks, landmark_regions, region_mapping_coordinates_all_frames, type)
        except:
            raise ValueError("frame ids provided not in the video. Please provide correct frame ids.")
    return region_mapping_coordinates_all_frames, landmark_regions


def mapperLandmarksToCordinatesEDMA(landmarks: dict, frames):
    """
    Maps landmarks to region-wise coordinates using the EDMA algorithm.

    Parameters:
        landmarks (dict): The input data containing landmarks.

    Returns:
        dict: The region-wise coordinates for all frames.

    """
    # Get the region-wise landmark mapping
    landmark_mapping = get_landmark_region_mapping()
    # Map landmarks to region-wise coordinates using normal mapping
    regionwiselandmarkmappedframes, region = landmarkMappingRegionwiseCoordinates(landmarks, landmark_mapping, frames, type="normal")
    # Return the region-wise coordinates
    return regionwiselandmarkmappedframes


def mapperLandmarksToCordinatesMirrorError(landmarks: dict, frames):
    """
    Maps landmarks to region-wise coordinates using the Mirror Error algorithm.

    Parameters:
        landmarks (dict): The input data containing landmarks.

    Returns:
        tuple: A tuple containing three elements:
            - region-wise coordinates for all frames using normal mapping
            - region-wise coordinates for all frames using reverse mapping
            - the region mapping used

    """
    # Get the region-wise landmark mapping
    # landmark_mapping = landmark_mapping_region_wise()
    landmark_mapping = get_landmark_region_mapping()
    # Map landmarks to region-wise coordinates using normal mapping
    regionwiselandmarkmappedframes, region = landmarkMappingRegionwiseCoordinates(landmarks, landmark_mapping, frames, type="normal")
    # Get the reverse region-wise landmark mapping
    landmark_mapping_reverse = get_landmark_region_mapping_reverse()
    # Map landmarks to region-wise coordinates using reverse mapping
    regionwiselandmarkmappedframesreverse, region = landmarkMappingRegionwiseCoordinates(landmarks, landmark_mapping_reverse, frames, type="reverse")
    # Return the region-wise coordinates and the region mapping
    return regionwiselandmarkmappedframes, regionwiselandmarkmappedframesreverse, region


def mouth_ul_ll_to_rm_lm(mo):
    # Rearrange the mouth landmarks to right-mouth and left-mouth regions
    left_mouth_bb_frame = mo[0:4] + mo[6:9] + mo[13:16] + mo[18:20]
    right_mouth_bb_frame = mo[3:6] + mo[8:14] + mo[16:19]
    return left_mouth_bb_frame, right_mouth_bb_frame


def get_landmark_region_mapping_reverse():
    return {"landmarkRegionMappingReverse": {
    "lb": [9,8,7,6,5],  
    "le": [28, 27, 26, 25, 30, 29],  
    "no": [10, 11, 12, 13, 18, 17, 16, 15, 14],  
    "rb": [4,3,2,1,0], 
    "re": [22, 21, 20, 19, 24, 23], 
    "mo": [37, 36, 35, 34, 33, 32, 47, 46, 45, 44, 31, 42, 41, 40, 39, 38, 43, 50, 49, 48]}} 

def get_landmark_region_mapping():
    return {"landmarkRegionMapping":{"lb": [0, 1, 2, 3, 4],  
    "rb": [5, 6, 7, 8, 9], 
    "no": [10, 11, 12, 13, 14, 15, 16, 17, 18],  
    "le": [19, 20, 21, 22, 23, 24], 
    "re": [25, 26, 27, 28, 29, 30], 
    "mo": [31, 32, 33, 34, 35, 36, 43, 44, 45, 46, 37, 38, 39, 40, 41, 42, 47, 48, 49, 50]}}
