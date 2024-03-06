from setuptools import setup, find_packages

setup(
    name='crisp_app',
    version='1.0.1',
    description='Crisp take-home assessment app that transforms uploaded input data using a config file',
    url="https://github.com/pdrogos02/crisp-take-home/",
    author='Peter Phyall',
    author_email='pdrogos02@gmail.com',
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires = ">=3.11",
    install_requires=[
        'pandas',
        'flask',
        'pyyaml',
        'werkzeug'
    ],
    extras_require={
        "test": ['pytest', 'coverage']
    },
    package_data={'crisp-take-home': ['data/schema.json']}
)