from bitbox.face_backend import FaceProcessor3DI

DIR = './'
input_file = DIR + 'data/elaine.mp4'
output_dir = DIR + 'output/'

processor = FaceProcessor3DI()

processor.io(input_file=input_file, output_dir=output_dir)

rects = processor.detect_faces()

lands = processor.detect_landmarks()

exp_global, pose, lands_can = processor.fit()

exp_local = processor.localized_expressions()