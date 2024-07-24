from bitbox.face_backend import FaceProcessor3DI
import os
from bitbox.expressions import symmetry
import json
from importlib import resources

"""
The symmetry function takes canonicalized landmarks and optional parameter frames as input and returns the symmetry scores based on mirror error and EDMA based approaches.

Scores closer to 0 indicate perfect symmetry, while scores further away from 0 indicate increasing degrees of asymmetry.

frames (list): A list of frame ids(integers from 0 to n) for which symmetry scores are to be calculated. Default is set to None, symmetry scores are calculated for all frames.

example:

frames = [1,2,10,20,30]

"""

# Set the directory path where the input file and output directory are located
#Please make sure you give the correct full (not relative) path

DIR = '/home/tuncb/Works/code/compsy/bitbox/tutorials'

# Specify the input file path
input_file = os.path.join(DIR, 'data/elaine.mp4')

# Specify the output directory path
output_dir = os.path.join(DIR, 'output')

# Create an instance of the FaceProcessor3DI class
processor = FaceProcessor3DI()

# Configure the input file and output directory for the processor
processor.io(input_file=input_file, output_dir=output_dir)

# Run all the processing steps on the input file
rect, land, exp_glob, pose, land_can, exp_loc = processor.run_all()

# Test the symmetry function using the canonicalized landmarks
# The function returns the symmetry scores based on mirror error and EDMA based approaches
symmetry_edma, symmetry_mirror_error = symmetry(land_can, frames=None)

"""

alterantively to test the symmetry functionality with the json file, you can use the following code:

lands_can = json.loads(resources.read_text('utilities.Resource_Files', 'landmark_test_input.json'))
    
"""