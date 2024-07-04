from setuptools import setup, find_packages

setup(
    name='pandas_ta',
    version='0.3.14b0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.5',
        'pandas>=1.1.5',
    ],
    description='Custom version of pandas_ta',
    license='MIT',
)
