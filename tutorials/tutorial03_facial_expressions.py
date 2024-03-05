from bitbox import FaceProcessor
from bitbox.expressions import symmetry, expressivity, diversity
from bitbox.coordination import cross_correlation

processor = FaceProcessor(input="/a/b/c/tbx001_ses-1_task-imitation.mp4", output="/d/e/f/", backend="3DI")

landmarks2D, landmarks3D, poses, expressions = processor.run_all()

exp_sym = symmetry(landmarks3D)
exp_exp = expressivity(landmarks3D)
exp_div = diversity(landmarks3D)

cor_intra_pose = cross_correlation(poses, poses)
cor_intra_exp = cross_correlation(expressions, expressions)