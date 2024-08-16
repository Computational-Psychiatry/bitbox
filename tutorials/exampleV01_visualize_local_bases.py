#!/usr/bin/python3.11

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os

#paths
video_file = 'data/elaine.mp4'
activations_file = 'output/elaine_expression_localized.3DI'
outputDIR = './'

# Get the filename from the video file path
filenamefull = os.path.basename(video_file)
# Get the filename without extension
filename = os.path.splitext(filenamefull)[0]
extension = os.path.splitext(filenamefull)[1]

# Load activations from text file
activations = np.loadtxt(activations_file)

# Load the video
cap = cv2.VideoCapture(video_file)

# Get video properties
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Split the activations into groups of action units
aus_idx = {'lb': (0,4),
           'rb': (4,8),
           'no': (8,12),
           'le': (12,16),
           're': (16,20),
           'ul': (20,25),
           'll': (25,32)}

facial_feats = list(aus_idx.keys())

groups = [activations[:, aus_idx[feat][0]:aus_idx[feat][1]] for feat in facial_feats]

def create_plot(group, up_to_frame):
    num_activations = group.shape[1]
    fig, axes = plt.subplots(num_activations, 1, figsize=(2*num_activations, 8))
    ymin = group[:, :].min()
    ymax = group[:, :].max()
    for idx, ax in enumerate(axes):
        ax.plot(group[:up_to_frame+1, idx])
        ax.set_xlim([0, frame_count])
        ax.set_ylim([ymin, ymax])
        if idx < num_activations - 1:
            ax.set_xticks([])
            ax.set_xlabel('')
    fig.tight_layout()
    canvas = FigureCanvas(fig)
    canvas.draw()
    img = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    img = img.reshape(canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return img

# Create videos
for i, group in enumerate(groups):
    # Define the codec and create VideoWriter object
    out_path = f'{outputDIR}/{filename}_{facial_feats[i]}.mp4'
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height + 600))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Rewind video to start

    for frame_idx in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Create the plot image
        plot_img = create_plot(group, frame_idx)

        # Resize plot image to match the video width
        plot_img = cv2.resize(plot_img, (frame_width, 600))

        # Concatenate video frame and plot image vertically
        combined_img = np.vstack((frame, plot_img))

        # Write the frame
        out.write(combined_img)

    out.release()
    
    print(f'Video {i+1} created successfully.')

cap.release()
cv2.destroyAllWindows()
