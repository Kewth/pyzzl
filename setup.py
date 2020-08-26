# from distutils.core import setup
from setuptools import setup
import os

setup(
    name='pyzzl',
    version='1.0',
    author='Kewth',
    author_email='Kewth.K.D@outlook.com',
    description='simple game',
    url='https://github.com/Kewth/pyzzl',
    package_dir={'pyzzl': 'source'},
    packages=['pyzzl'],
    install_requires=[
    ],
    data_files=[
        ('share/pyzzl', []),
        ('bin', ['pyzzl']),
    ],
    )
