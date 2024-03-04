from bitbox import FaceProcessor

processor = FaceProcessor(input="/a/b/c/tbx001_ses-1_task-imitation.mp4", output="/d/e/f/", backend="3DI")

landmarks2D, landmarks3D, poses, expressions = processor.run_all()

