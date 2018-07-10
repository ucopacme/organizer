#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __init__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'org/__init__.py')) as f:
    exec(f.read(), about)

setup(
    name='organizer',
    version=about['__version__'],
    description='Tools for working with AWS Organizations',
    long_description=long_description,
    url='https://github.com/ucopacme/organizer',
    keywords='aws organizations boto3',
    author='Ashley Gould',
    author_email='agould@ucop.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'botocore',
        'boto3',
        'PyYAML',
    ],
    packages=find_packages(
        '.',
        exclude=[
            'tests',
            'examples',
            'RELEASE.rst'
        ],
    ),
    include_package_data=True,
    zip_safe=False,
)

