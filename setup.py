# make sure that 'aws configure --profile SAME TO ALL OTHER STATION'
from setuptools import setup

setup(
    name='snaplyzer1',
    version='0.1',
    author="Rick Zheng",
    author_email="rick.zheng@gmail.com",
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