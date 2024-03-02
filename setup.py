from setuptools import setup, find_packages

setup(
    name='crisp-app',
    version='1.0.0',
    description='app that transforms per uploaded input data and config file',
    author='Peter Phyall',
    author_email='pdrogos02@gmail.com',
    packages=find_packages(where="src"),
    install_requires=[
        'pandas',
        'flask',
        'pyyaml',
        'werkzeug'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest', 'coverage'],
    package_data={'crisp-take-home': ['data/schema.json']}
)