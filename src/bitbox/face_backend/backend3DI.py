import os
import warnings

import numpy as np

from time import time

from ..utilities import FileCache

from .functions3DI import save_shape_and_texture
from .functions3DI import total_variance_rec, total_variance_rec_pose
from .functions3DI import compute_canonicalized_landmarks, compute_localized_expressions

from .reader3DI import read_rectangles, read_landmarks
from .reader3DI import read_pose, read_expression, read_canonical_landmarks

class FaceProcessor3DI:
    def __init__(self, camera_model=30, landmark_model='global4', morphable_model='BFMmm-19830', fast=False, return_dict=True):
        self.file_input = None
        self.dir_output = None
        self.execDIR = None
        self.base_metadata = None
        
        self.model_camera = camera_model
        self.model_morphable = morphable_model
        self.model_landmark = landmark_model
        self.fast = fast
        
        self.cache = FileCache()
        
        self.return_dict = return_dict
        
        # find out where 3DI package is installed
        if os.environ.get('PATH_3DI'):
            execDIRs = [os.environ.get('PATH_3DI')]
        else:
            warnings.warn("PATH_3DI environment variable is not set. Using default system PATH.")
            execDIRs = os.environ.get('PATH')
            if ';' in execDIRs:  # Windows
                execDIRs = execDIRs.split(';')
            else:  # Unix-like systems (Linux, macOS)
                execDIRs = execDIRs.split(':')
                
        for d in execDIRs:
            if os.path.exists(d + '/video_learn_identity'):
                self.execDIR = d + '/'
                break
            
        if self.execDIR is None:
            raise ValueError("3DI package is not found. Please make sure you defined PATH_3DI system variable.")
        
        # set the working directory
        # @TODO: remove this line when the 3DI code is updated by Vangelis
        os.chdir(self.execDIR)
        
        # prepare configuration files
        if self.fast:
            cfgid = 2
        else:
            cfgid = 1
        
        self.config_landmarks = self.execDIR + 'configs/%s.cfg%d.%s.txt' % (self.model_morphable, cfgid, self.model_landmark)
    
    
    def _shape_and_texture(self, shp_path, tex_path):
        alpha = np.loadtxt(self.file_shape_coeff)
        beta =  0.4*np.loadtxt(self.file_texture_coeff)
        sdir = self.execDIR + 'models/MMs/%s' % self.model_morphable
        
        save_shape_and_texture(alpha, beta, sdir, shp_path, tex_path)
    
    
    def _smooth_expression(self, exp_path, exp_path_new):
        total_variance_rec(self.execDIR, exp_path, exp_path_new, self.model_morphable)
    
    
    def _smooth_pose(self, pose_path, pose_path_new):
        total_variance_rec_pose(pose_path, pose_path_new)
        
    
    def _canonicalized_landmarks(self, exp_path, exp_path_new):
        compute_canonicalized_landmarks(self.execDIR, exp_path, exp_path_new, self.model_morphable)
    
    
    def _local_expressions(self, land_path, exp_path):
        compute_localized_expressions(self.execDIR, land_path, exp_path, self.model_morphable)
    
    
    def _execute(self, executable, parameters, name, output_file_idx=-1, system_call=True):
        status = False
        
        # get the output file name
        if not isinstance(output_file_idx, list):
            output_file_idx = [output_file_idx]
       
        # check if the output file already exists, if not run the executable
        self.base_metadata = {
            'backend' : '3DI',
            'morphable_model': self.model_morphable,
            'camera': self.model_camera,
            'landmark': self.model_landmark,
            'fast': self.fast
        }  
        
        file_exits = 0
        for idx in output_file_idx:
            tmp = self.cache.check_file(parameters[idx], self.base_metadata, verbose=True)
            file_exits = max(file_exits, tmp)
        
        # run the executable if needed
        if file_exits > 0: # file does not exist, has different metadata, or it is older than the retention period
            # if needed, change the name of the output file
            # @TODO: when we change the file name, next time we run the code, we should be using the latest file generated, which is hard to track. We are rewriting for now.
            # @TODO: for the same reason above, we need to remove the old metadata file otherwise "file_generated" will be >0 and fail the check
            # @TODO: also we need to consider multiple output files
            if file_exits == 2:
                # delete this loop after resolving above @TODO
                for idx in output_file_idx:
                    self.cache.delete_old_file(parameters[idx])
                #output_file = self.cache.get_new_file_name(output_file)  # uncomment after resolving above @TODO
                #parameters[output_file_idx] = output_file  # uncomment after resolving above @TODO
            
            # run the command
            print("Running %s..." % name, end='')
            t0 = time()
            
            if system_call: # if we are using system call
                # prepare the command
                cmd = self.execDIR + executable
                for p in parameters:
                    if p is None:
                        raise ValueError("File names are not set correctly. Please use io() method prior to running any processing.")
                    cmd += ' ' + str(p)
                # suppress the output of the command. check whether we are on a Windows or Unix-like system
                if os.name == 'nt': # Windows
                    cmd += ' > NUL'
                else: # Unix-like systems (Linux, macOS)
                    cmd += ' > /dev/null'            
                os.system(cmd)
            else: # if we are using a python function
                cmd = "%s()" % executable
                # prepare the function
                func = getattr(self, executable)
                func(*parameters)
            
            print(" (Took %.2f secs)" % (time()-t0))
            
            # check if face detection was successful
            file_generated = 0
            for idx in output_file_idx:
                tmp = self.cache.check_file(parameters[idx], self.base_metadata, verbose=False, json_required=False, retention_period='5 minutes')
                file_generated = max(file_generated, tmp)
            
            if file_generated == 0: # file is generated (0 means the file is found)
                # store metadata
                additional_metadata = {
                    'cmd': cmd,
                    'input': self.file_input,
                    'output': self.dir_output
                }
                metadata = {**self.base_metadata, **additional_metadata}
                for idx in output_file_idx:
                    self.cache.store_metadata(parameters[idx], metadata)
                    
                status = True
            else:
                status = False
        else: # file is already present
            status = True
            
        if not status:
            raise ValueError("Failed running %s" % name)
    
        
    def io(self, input_file, output_dir):
        # supported video extensions
        supported_extensions = ['mp4', 'avi', 'mpeg']

        # check if input file exists
        if not os.path.exists(input_file):
            raise ValueError("Input file does not exist. Please check the path and permissions.")
        
        # check if input file extension is supported
        ext = input_file.split('.')[-1].lower()
        if not (ext in supported_extensions):
            raise ValueError("Input file extension is not supported. Please use one of the following extensions: %s" % supported_extensions)
        
        # create output directory
        try:
            os.makedirs(output_dir, exist_ok=True)
        except:
            raise ValueError("Cannot create output directory. Please check the path and permissions.")  
 
        # if no exception is raised, set the input file and output directory
        self.file_input = input_file
        self.file_input_base = '.'.join(os.path.basename(input_file).split('.')[:-1])
        self.dir_output = output_dir + '/'
        
        # set all the output files
        self.file_input_prep = self.dir_output + self.file_input_base + '_preprocessed.' + ext # preprocessed video file
        self.file_rectangles = self.dir_output + self.file_input_base + '_rects.3DI' # face rectangles
        self.file_landmarks = self.dir_output + self.file_input_base + '_landmarks.3DI' # landmarks
        self.file_shape_coeff  = self.dir_output + self.file_input_base + '_shape_coeff.3DI' # shape coefficients
        self.file_texture_coeff  = self.dir_output + self.file_input_base + '_texture_coeff.3DI' # texture coefficients
        self.file_shape  = self.dir_output + self.file_input_base + '_shape.3DI' # shape model
        self.file_texture  = self.dir_output + self.file_input_base + '_texture.3DI' # texture model
        self.file_expression  = self.dir_output + self.file_input_base + '_expression.3DI' # expression coefficients
        self.file_pose  = self.dir_output + self.file_input_base + '_pose.3DI' # pose info
        self.file_illumination  = self.dir_output + self.file_input_base + '_illumination.3DI' # illumination coefficients
        self.file_expression_smooth = self.dir_output + self.file_input_base + '_expression_smooth.3DI' # smoothed expression coefficients
        self.file_pose_smooth = self.dir_output + self.file_input_base + '_pose_smooth.3DI' # smoothed pose info
        self.file_landmarks_cannonicalized = self.dir_output + self.file_input_base + '_landmarks_cannonicalized.3DI' # canonicalized landmarks
        self.file_expression_localized = self.dir_output + self.file_input_base + '_expression_localized.3DI' # localized expressions
               
        
    def preprocess(self, undistort=True):
        # run undistortion if needed
        if undistort==True:
            # check if proper camera parameters are provided
            # @TODO: check if self.model_camera is a valid file and includes undistortion parameters
            
            self._execute('video_undistort',
                                   [self.file_input, self.model_camera, self.file_input_prep],
                                   "video undistortion",
                                   output_file_idx=-1)
        
            self.file_input = self.file_input_prep
            
            
    def detect_faces(self):
        self._execute('video_detect_face',
                      [self.file_input, self.file_rectangles],
                      "face detection",
                      output_file_idx=-1)
               
        if self.return_dict:
            return read_rectangles(self.file_rectangles)
            
            
    def detect_landmarks(self):
        # check if face detection was run and successful
        if self.cache.check_file(self.file_rectangles, self.base_metadata) > 0:
            raise ValueError("Face detection is not run or failed. Please run face detection first.")
        
        self._execute('video_detect_landmarks',
                      [self.file_input, self.file_rectangles, self.file_landmarks, self.config_landmarks],
                      "landmark detection",
                      output_file_idx=-2)
        
        if self.return_dict:
            return read_landmarks(self.file_landmarks)
        

    def fit(self):
        # check if landmark detection was run and successful
        if self.cache.check_file(self.file_landmarks, self.base_metadata) > 0:
            raise ValueError("Landmark detection is not run or failed. Please run landmark detection first.")
     
        # STEP 1: learn identity   
        self._execute('video_learn_identity',
                      [self.file_input, self.file_landmarks, self.config_landmarks, self.model_camera, self.file_shape_coeff, self.file_texture_coeff],
                      "3D face model fitting",
                      output_file_idx=[-2, -1])
     
        # STEP 2: shape and texture model
        self._execute('_shape_and_texture',
                      [self.file_shape, self.file_texture],
                      "shape and texture model",
                      output_file_idx=[-2, -1],
                      system_call=False)

        # STEP 3: Pose and expression
        self._execute('video_from_saved_identity',
                      [self.file_input, self.file_landmarks, self.config_landmarks, self.model_camera, self.file_shape, self.file_texture, self.file_expression, self.file_pose, self.file_illumination],
                      "expression and pose estimation",
                      output_file_idx=[-3, -2, -1])

        # STEP 4: Smooth expression and pose
        self._execute('_smooth_expression',
                    [self.file_expression, self.file_expression_smooth],
                    "expression smoothing",
                    output_file_idx=-1,
                    system_call=False)
        
        self._execute('_smooth_pose',
                    [self.file_pose, self.file_pose_smooth],
                    "pose smoothing",
                    output_file_idx=-1,
                    system_call=False)
            
        # STEP 5: Canonicalized landmarks
        self._execute('_canonicalized_landmarks',
                    [self.file_expression_smooth, self.file_landmarks_cannonicalized],
                    "canonicalized landmark estimation",
                    output_file_idx=-1,
                    system_call=False)
        
        if self.return_dict:
            return read_expression(self.file_expression_smooth), read_pose(self.file_pose_smooth), read_canonical_landmarks(self.file_landmarks_cannonicalized)
        

    def localized_expressions(self):
        # check if canonical landmark detection was run and successful
        if self.cache.check_file(self.file_landmarks_cannonicalized, self.base_metadata) > 0:
            raise ValueError("Canonical landmark detection is not run or failed. Please run fit() method first.")
        
        self._execute('_local_expressions',
                    [self.file_landmarks_cannonicalized, self.file_expression_localized],
                    "localized expression estimation",
                    output_file_idx=-1,
                    system_call=False)
        
        return np.loadtxt(self.file_expression_localized)


    def run_all(self, undistort=False):
        self._check_configuration()
        return 0, 0, 0, 0
    
    
    
    # alpha_sm = 0.70*np.loadtxt(self.file_shape_coeff)
    # beta_sm =  0.70*np.loadtxt(self.file_texture_coeff)
    # if not os.path.exists(shpsm_fpath) or not os.path.exists(texsm_fpath):
    #     save_identity_and_shape(alpha_sm, beta_sm, shpsm_fpath, texsm_fpath, morphable_model)