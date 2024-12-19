# Base image including 3DI but not the face model file
FROM compsydocker/3di:20241217-opencv4.7.0-cuda12.0.0-cudnn8-devel-ubuntu22.04

# Add the model file and prepare it to be used by 3DI
COPY 01_MorphableModel.mat /app/build/models/raw/
RUN cd /app/build/models && python3 prepare_BFM.py