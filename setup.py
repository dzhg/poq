#!/usr/bin/env python

from distutils.core import setup

setup(name='poq',
      version='0.1.0',
      description='Python Object Query Utility',
      author='Di Zhang',
      author_email='daniel.di.zhang@gmail.com',
      packages=['poq'], requires=['ply'],
      install_requires=["ply>=3.1.0,<4"]
      )
