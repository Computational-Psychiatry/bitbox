from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'bitbox',
    version = '2024.03dev1',
    description = 'Behavioral Imaging Toolbox',
    author = 'ComPsy Group',
    author_email = 'tuncb@chop.edu',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Computational-Psychiatry/bitbox',
    license = 'GPL-3.0',
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires = '>=3.8',
    install_requires = [
        'numpy',
        'cvxpy',
        'scikit-learn'
    ]
)
