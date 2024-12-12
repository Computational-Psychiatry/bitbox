# Behavioral Imaging Toolbox

Bitbox is a free and open-source Python library including a comprehensive set of tools for the computational analysis of nonverbal human behavior. The provided tools enable analysis of face, head, and body movements, expressions, and actions from videos and images. Included algorithms and metrics have been validated using clinically vetted datasets and published extensively, therefore, can be reliably used by behavioral, social, and medical scientists in their human subject research. As we closely follow state-of-the-art in computer vision and machine learning, provided methodologies can also be relied upon by computer vision researchers and other engineers as well.

Please refer to our [Wiki](https://github.com/Computational-Psychiatry/bitbox/wiki) for further details.

## Installation

Bitbox itself has minimum requirements, but it relies on face/body backends to generate expression/movement signals. These backends usually have more requirements. We highly recommend using our Docker images to install these backends as installing them from source code may prove difficult for some. 

### Installing Face Backends 

The current version of Bitbox supports two face backends, namely 3DI and 3DI-lite, for systems with and without GPU supports, respectively. While 3DI-lite is easier to install, faster, and in some cases, more robust to occlusions, etc., we recommend using 3DI as it is a more generic algorithm, and it may have higher reliability and validity with most videos/images. Nevertheless, if you cannot use NVIDIA GPUs, for example, if you are working on a Mac or a system with AMD GPUs, you need to use 3DI-lite.

If you can install C++/CUDA codes from the source code, please go ahead and install 3DI from [https://github.com/Computational-Psychiatry/3DI](https://github.com/Computational-Psychiatry/3DI). The instructions are provided there. This approach will install the 3DI as a native application on your system and will be more convenient for using Bitbox.

Similarly, 3DI-lite can be installed from ... (COMING SOON)

The recommended way to install backends is to use our Docker images. Using Docker is usually very straightforward; however, 3DI requires downloading an external face model (you need to register individually and request access) and updating our image with this model. Thus, there are a few extra steps you need to do. We provide two options for this.

#### Using Docker: Option 1 

... (COMING SOON)

#### Using Docker: Option 2 

... (COMING SOON)

### Installing Bitbox
To install Bitbox, follow these steps. **You will need to use python 3.8 or higher**. 

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

