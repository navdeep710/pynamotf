#!/usr/bin/env python

from distutils.core import setup

setup(
  name='pynamotf',
  version='0.1',
  description='Terraform harness for pynamodb dynamo mapper',
  author='Abe Winter',
  author_email='awinter.public@gmail.com',
  packages=['pynamotf'],
  install_requires=['pynamodb'],
  entry_points={
    'console_scripts': ['pynamotf=pynamotf.__main__:main'],
  },
)

