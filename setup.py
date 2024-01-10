from setuptools import setup, find_packages

setup(
    name='fetch_tlc_taxi_data',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests=2.31.0',
        'pandas=2.1.4',
        'beautifulsoup4=4.12.2',
        'pyarrow=14.0.2',
        'lxml=5.1.0',
        'openpyxl=3.1.2'
    ],
)