# Behavioral Imaging Toolbox

Bitbox is a free and open-source Python library including a comprehensive set of tools for the computational analysis of nonverbal human behavior. The provided tools enable analysis of face, head, and body movements, expressions, and actions from videos and images. Included algorithms and metrics have been validated using clinically vetted datasets and published extensively, therefore, can be reliably used by behavioral, social, and medical scientists in their human subject research. As we closely follow state-of-the-art in computer vision and machine learning, provided methodologies can also be relied upon by computer vision researchers and other engineers as well.

Please refer to our [Wiki](https://github.com/Computational-Psychiatry/bitbox/wiki) for further details.

## Installation

Before installing Bitbox, you need to install 3DI. If 3DI is not installed, you will receive an error when trying to use Bitbox. 3DI repository is located at [https://github.com/Computational-Psychiatry/3DI](https://github.com/Computational-Psychiatry/3DI). **You will need to use python 3.8 or higher**. 

To install Bitbox, follow these steps:

1. Create a virtual environment and activate it:
    ```bash
    python3.8 -m venv env
    source env/bin/activate
    ```
    Note that this will create a virtual environment named `env` in the current directory. You can use any name, and you can install the virtual environment anywhere you like. Just don't forget where you installed it. For the following steps, we will assume you have activated the virtual environment.

2. Clone the Bitbox repository:
    ```bash
    git clone https://github.com/Computational-Psychiatry/bitbox.git
    ```

3. Change to the Bitbox directory:
    ```bash
    cd bitbox
    ```

4. Install requirements:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

5. Install Bitbox using `python setup.py install`:
    ```bash
    python setup.py install
    ```

6. Set the environment variable `PATH_3DI` to indicate the directory in which 3DI was installed:

    - **Linux**:
      ```bash
      export PATH_3DI=/path/to/3DI/directory
      ```

    - **Windows** (Command Prompt):
      ```bash
      set PATH_3DI=C:\path\to\3DI\directory
      ```

    - **Mac**:
      ```bash
      export PATH_3DI=/path/to/3DI/directory
      ```

Now you are ready to use Bitbox!

## Use

Once you are done with installation, you can use Bitbox by

1. Activate the virtual environment you created for Bitbox:
    ```bash
    source env/bin/activate
    ```
2. Set the environment variable `PATH_3DI`. You need to do this only if you did not set it in .bahsrc (on Lunux/Mac) or in System's Environment Variables (on Windows). If you did that you can skip this step.

3. Import the library in your Python code:
 ```python
from bitbox.face_backend import FaceProcessor3DI
import os

# Please make sure you give the correct full (not relative) path
DIR = '/path/to/tutorials'
input_file = os.path.join(DIR, 'data/elaine.mp4') 
output_dir = os.path.join(DIR, 'output')

# define a face processor
processor = FaceProcessor3DI()

# set input and output
processor.io(input_file=input_file, output_dir=output_dir)

# detect faces
rects = processor.detect_faces()

# detect landmarks
lands = processor.detect_landmarks()

# compute global expressions
exp_global, pose, lands_can = processor.fit()

# compute localized expressions
exp_local = processor.localized_expressions()
 ```

