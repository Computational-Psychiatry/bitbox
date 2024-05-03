# Behavioral Imaging Toolbox

Bitbox is a free and open-source Python library including a comprehensive set of tools for the computational analysis of nonverbal human behavior. The provided tools enable analysis of face, head, and body movements, expressions, and actions from videos and images. Included algorithms and metrics have been validated using clinically vetted datasets and published extensively, therefore, can be reliably used by behavioral, social, and medical scientists in their human subject research. As we closely follow state-of-the-art in computer vision and machine learning, provided methodologies can also be relied upon by computer vision researchers and other engineers as well.

Please refer to our [Wiki](https://github.com/Computational-Psychiatry/bitbox/wiki) for further details.

## Installation

Before installing Bitbox, you need to install 3DI. If 3DI is not installed, you will receive an error when trying to use Bitbox. 3DI repository is located at [https://github.com/Computational-Psychiatry/3DI](https://github.com/Computational-Psychiatry/3DI).

To install Bitbox, follow these steps:

1. Clone the Bitbox repository:
    ```bash
    git clone https://github.com/Computational-Psychiatry/bitbox.git
    ```

2. Change to the Bitbox directory:
    ```bash
    cd bitbox
    ```

3. Install Bitbox using `python setup.py install`:
    ```bash
    python setup.py install
    ```

4. Set the environment variable `PATH_3DI` to indicate the directory in which 3DI was installed:

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

Template for the Read the Docs tutorial
=======================================

This GitHub template includes fictional Python library
with some basic Sphinx docs.

Read the tutorial here:

https://docs.readthedocs.io/en/stable/tutorial/