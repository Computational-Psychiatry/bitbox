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

#### Using Docker: Option 1 (Recommended)

We have a pre-compiled Docker image for 3DI, but with a specific CUDA driver (i.e., 12.0.0). If your GPU can work with this version of CUDA, please use this option. Otherwise, you need to use the second option below.

1. Download the [Dockerfile](https://github.com/Computational-Psychiatry/3DI/raw/main/docker/3DI/Dockerfile)
2. Download the [3DMM model](https://faces.dmi.unibas.ch/bfm/index.php?nav=1-2&id=downloads)
3. Place the Dockerfile and the face model (`01_MorphableModel.mat`) in the same directory
4. Within this directory, run the following command to copy the face model
    ```bash
    docker build -t 3di:basel2009-20241217 . 
    ```
    The first parameter `3di:basel2009-20241217` is the name of the name image to be created. You can replace it if you wish. Please don't forget the `.` at the end. 
5. That's it! You will also need to set an environment variable `DOCKER_3DI`, which will be explained below.

#### Using Docker: Option 2 (Only for advanced Docker users)

If your system (GPUs) cannot work with CUDA 12.0.0, and if you still want to use Docker, you will need to download our base Dockerfile, modify it for your needs, and compile it. This option, however, will require running every steps that are necessary for installing 3DI from source. Thus, unless you have an actual reason to use Docker (e.g., you cannot install CUDA or any other packages on your system, you don't have admin rights, etc.), we recommend installing 3DI from source natively on your system, as this may yield a slightly faster 3DI. 

1. Download the [Dockerfile](https://github.com/Computational-Psychiatry/3DI/raw/main/docker/3DI_base/Dockerfile)
2. Download the [3DMM model](https://faces.dmi.unibas.ch/bfm/index.php?nav=1-2&id=downloads)
3. Place the Dockerfile and the face model (01_MorphableModel.mat) in the same directory
4. Modify the Dockerfile to fit it to your system. Specifically,
    1. Change the following line to start from a specific CUDA image. You will need to change the image tag `compsydocker/3di:cuda12.0.0-cudnn8-devel-ubuntu22.04-base`. You can find an available tag from [NVIDIA's CUDA images](https://hub.docker.com/r/nvidia/cuda/tags). Example: `nvidia/cuda:12.6.3-cudnn-devel-ubuntu20.04`
    ```bash
    FROM compsydocker/3di:cuda12.0.0-cudnn8-devel-ubuntu22.04-base
    ```
    2. Change the following lines to compile a specific openCV version that works with your CUDA version. Unfortunately, you have to "discover" the exact version yourself. You may need to change the `cmake` parameters below these lines as well.
    ```bash
    RUN git clone --branch 4.7.0 --depth 1 https://github.com/opencv/opencv.git && \
        git clone --branch 4.7.0 --depth 1 https://github.com/opencv/opencv_contrib.git && \
    ```
5. Once you finished modifying the Dockerfile and verify it is working (you may need to run docker interactively for this purpose), run the following command within the same directory
    ```bash
    docker build -t 3di:basel2009-20241217 . 
    ```
    The first parameter `3di:basel2009-20241217` is the name of the name image to be created. You can replace it if you wish. Please don;t forget the `.` at the end.
6. If you feel you will enjoy helping us and others, you may also share your tested and verified Dockerfile with us so that we can serve this modified image with others as well.
7. That's it! You will also need to set an environment variable `DOCKER_3DI`, which will be explained below.

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

6. If you are not using Docker, set the environment variable `PATH_3DI` to indicate the directory in which 3DI was installed. We recommend setting it in .bahsrc (on Lunux/Mac) or in System's Environment Variables (on Windows).

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

7. If you are using Docker, set the environment variable `DOCKER_3DI` to indicate the 3DI image name/tag. Change the image name/tag if needed. We recommend setting it in .bahsrc (on Lunux/Mac) or in System's Environment Variables (on Windows).

    - **Linux**:
      ```bash
      export DOCKER_3DI=3di:basel2009-20241217
      ```

    - **Windows** (Command Prompt):
      ```bash
      set DOCKER_3DI=3di:basel2009-20241217
      ```

    - **Mac**:
      ```bash
      export DOCKER_3DI=3di:basel2009-20241217
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

