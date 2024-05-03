# API Reference

## FaceProcessor3DI

### `class FaceProcessor3DI(camera_model=30, landmark_model='global4', morphable_model='BFMmm-19830', fast=False, return_dict=True)`
Provides the main interface for facial analysis, enabling detailed 3D modeling for comprehensive behavioral analysis.

#### Parameters:
- **camera_model** (`int` or `str`, optional): Represents the field of view or path to camera specs, default is `30`.
- **landmark_model** (`str`, optional): Specifies the facial landmark model, default is `'global4'`.
- **morphable_model** (`str`, optional): Specifies the 3D morphable model used for facial reconstructions, default is `'BFMmm-19830'`.
- **fast** (`bool`, optional): Toggles between detailed and faster, less detailed analysis, default is `False`.
- **return_dict** (`bool`, optional): Determines the format of the results returned, default is `True`.

#### Note:
If `camera_model` is an integer, the `undistort` method cannot be used.

### Methods

#### `__init__(self, camera_model=30, landmark_model='global4', morphable_model='BFMmm-19830', fast=False, return_dict=True)`
Initializes the FaceProcessor3DI object with the specified camera, landmark, and morphable models. Configures processing speed and output format.
- **camera_model** (`int` or `str`, optional): Field of view or filepath for camera specs, default is `30`.
- **landmark_model** (`str`, optional): Facial landmark model used, default is `'global4'`.
- **morphable_model** (`str`, optional): 3D morphable model for face reconstruction, default is `'BFMmm-19830'`.
- **fast** (`bool`, optional): If `True`, uses a faster, less detailed landmark model, default is `False`.
- **return_dict** (`bool`, optional): Output format choice, returns a dictionary if `True`, default is `True`.

#### `_shape_and_texture(self, shp_path, tex_path)`
Processes shape and texture coefficients to save 3D shape and texture models at the specified paths.
- **shp_path** (`str`): File path to save the 3D shape model.
- **tex_path** (`str`): File path to save the 3D texture model.

#### `_smooth_expression(self, exp_path, exp_path_new)`
Applies a variance reduction technique to smooth facial expressions data, saving the results to a new path.
- **exp_path** (`str`): File path of the original expression data.
- **exp_path_new** (`str`): File path to save the smoothed expression data.

#### `_smooth_pose(self, pose_path, pose_path_new)`
Smooths pose data by applying a variance reduction technique and saves the smoothed data to a new file.
- **pose_path** (`str`): File path of the original pose data.
- **pose_path_new** (`str`): File path to save the smoothed pose data.

#### `_canonicalized_landmarks(self, exp_path, exp_path_new)`
Computes and saves canonicalized landmarks based on the expression data at the specified new path.
- **exp_path** (`str`): File path containing expression data.
- **exp_path_new** (`str`): File path to save the canonicalized landmarks.

#### `_local_expressions(self, land_path, exp_path)`
Calculates and saves localized expressions from canonicalized landmarks.
- **land_path** (`str`): File path containing canonicalized landmarks.
- **exp_path** (`str`): File path to save the localized expressions.

#### `_execute(self, executable, parameters, name, output_file_idx, system_call)`
Executes the specified process, either as a system call or a Python function. Manages file checks, creation, and metadata storage.
- **executable** (`str`): Name or path of the executable or function.
- **parameters** (`list`): List of parameters to pass to the executable.
- **name** (`str`): Human-readable name of the process for logging.
- **output_file_idx** (`int` or `list`): Index(es) in the parameters list that refer to output file paths.
- **system_call** (`bool`): Whether to execute as a system call or a Python function call.

#### `io(self, input_file, output_dir)`
Sets up and verifies input and output file paths for video processing. Initializes paths for various output files based on the input.
- **input_file** (`str`): Path to the video file to be processed.
- **output_dir** (`str`): Directory path where output files will be saved.

#### `preprocess(self, undistort)`
Preprocesses the video file, optionally undistorting it based on the specified camera parameters.
- **undistort** (`bool`): Whether to apply undistortion based on the camera model.

#### `detect_faces(self)`
Detects faces in the video and, if `return_dict` is True, returns the bounding boxes of detected faces.
- No parameters required.

#### `detect_landmarks(self)`
Detects facial landmarks using the configured landmark model, following successful face detection.
- No parameters required.

#### `fit(self)`
Performs a series of operations to fit a 3D face model to the detected landmarks, including smoothing and canonicalization steps. Returns JSON objects for smoothed expressions, poses, and canonical landmarks if `return_dict` is True.
- No parameters required.

#### `localized_expressions(self)`
Estimates and returns localized expressions using canonicalized landmarks, following successful face model fitting.
- No parameters required.

#### `run_all(self, undistort)`
Executes the entire pipeline from preprocessing the video to estimating localized expressions. 
- **undistort** (`bool`): Whether to apply undistortion as part of preprocessing.

### Functions

#### `read_rectangles(file_path)`
Reads bounding box data from a file.
- **file_path** (`str`): Path to the file containing bounding box data.

#### `read_landmarks(file_path)`
Reads facial landmark data from a file.
- **file_path** (`str`): Path to the file containing landmark data.

#### `read_pose(file_path)`
Reads pose data from a file.
- **file_path** (`str`): Path to the file containing pose data.

#### `read_expression(file_path)`
Reads facial expression data from a file.
- **file_path** (`str`): Path to the file containing expression data.

#### `read_canonical_landmarks(file_path)`
Reads canonical landmarks data from a file.
- **file_path** (`str`): Path to the file containing canonical landmark data.
