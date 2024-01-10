from setuptools import setup, find_packages

setup(
    name='fetch_tlc_taxi_data',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'beautifulsoup4',
        'pyarrow',
        'lxml',
        'openpyxl'
    ],
)