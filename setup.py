#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
import slashcommands


setup(
    # meta information
    name='slashcommands',
    version=slashcommands.__version__,
    description='A tiny framework for slash commands of Slack.',
    long_description=slashcommands.__doc__,
    url='https://github.com/matsub/slashcommands',
    license='MIT',

    author=slashcommands.__author__,
    author_email='matsub.rk@gmail.com',

    # include all packages
    packages=find_packages(exclude=['tests', 'wercker.yml']),
    include_package_data=True,

    install_requires=[
        'japronto==0.1.1',
    ],
)
