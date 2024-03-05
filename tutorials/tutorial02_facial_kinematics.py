from bitbox import FaceProcessor
from bitbox.kinematics import spatial_extent, speed, smoothness

processor = FaceProcessor(input="/a/b/c/tbx001_ses-1_task-imitation.mp4", output="/d/e/f/", backend="3DI")

landmarks2D, landmarks3D, poses, expressions = processor.run_all()

kinm_spe = spatial_extent(landmarks2D)
kinm_spd = speed(landmarks2D)
kinm_smt = smoothness(landmarks2D)