#!/usr/bin/env python

from distutils.core import setup

setup(
    name='relaax',
    version='0.1',
    description='RELAAX solution',
    author='Stanislav Volodarskiy',
    author_email='stanislav@dplrn.com',
    url='http://www.dplrn.com/',
    packages=['relaax'],
    install_requires=[
        'ruamel.yaml',
        'futures',
        'grpcio_tools',
        'grpcio',
        'boto3',
        'pillow',
        'numpy',
        'scipy',
        'psutil',
        'honcho',
        'keras',
        'h5py',
        'mock',
        'tensorflow==0.12.1'
    ],
    provides=['relaax'],
    scripts=[
        'bin/relaax-parameter-server',
        'bin/relaax-rlx-server'
    ]
)
