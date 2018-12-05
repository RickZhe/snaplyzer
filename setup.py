# setup.py
from setuptools import setup

setup(
    name='snaplyzer_300',
    version='0.1',
    auther='Rick Zheng',
    auther_email="rick.zheng@gmail.com",
    description="snaplyzer is tools manage AWS EC2 snapshots",
    license="GPLv3+",
    packages=['snaplyzer'],
    url="https://github.com/RickZhe/snaplyzer",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        snaplyzer=snaplyzer.snaplyzer:cli
    ''',


)