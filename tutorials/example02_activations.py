from bitbox.face_backend import FaceProcessor3DI
from bitbox.signal_processing import peak_detection
from bitbox.coordination import intra_person_coordination

import os
import numpy as np

# Please make sure you give the correct full (not relative) path
DIR = '/home/tuncb/Works/code/compsy/bitbox/tutorials'
input_file = os.path.join(DIR, 'data/elaine.mp4')
output_dir = os.path.join(DIR, 'output')

processor = FaceProcessor3DI()

processor.io(input_file=input_file, output_dir=output_dir)

rect, land, exp_glob, pose, land_can, exp_loc = processor.run_all()

data = np.array(list(exp_loc['data'].values())).astype('float')

peaks = peak_detection(data[:,33], num_scales=6, fps=30, smooth=True, visualize=True)

corr_mean, corr_lag, corr_std = intra_person_coordination(exp_loc, width=0.5, fps=30)

