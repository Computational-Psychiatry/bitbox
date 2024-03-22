# Behavioral Imaging Toolbox

Bitbox is a free and open-source Python library including a comprehensive set of tools for the computational analysis of nonverbal human behavior. The provided tools enable analysis of face, head, and body movements, expressions, and actions from videos and images. Included algorithms and metrics have been validated using clinically vetted datasets and published extensively, therefore, can be reliably used by behavioral, social, and medical scientists in their human subject research. As we closely follow state-of-the-art in computer vision and machine learning, provided methodologies can also be relied upon by computer vision researchers and other engineers as well.

Please refer to our [Wiki](https://github.com/Computational-Psychiatry/bitbox/wiki) for further details.

## Installation

Before installing Bitbox, you need to install 3DI. If 3DI is not installed, you will receive an error when trying to use Bitbox. 3DI repository is located at [https://github.com/Computational-Psychiatry/3DI](https://github.com/Computational-Psychiatry/3DI).

To install Bitbox, follow these steps:

1. Create a virtual environment and activate it:
    ```bash
    python3 -m venv bitbox
    source bitbox/bin/activate
    ```
    Note that this will create a virtual environment named "bitbox" in the current directory. You can use any name, and you can install the virtual environment anywhere you like. Just don't forget where you installed it. For the following steps, we will assume you have activated the virtual environment.

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



