#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages


LONGDESC = '''
Getting Started with OrgCrawler
===============================

A python library for managing resources across all accounts in an AWS Organization.

OrgCrawler package exports two primary classes:

``orgcrawler.orgs.Org``
  provides a data model and methods for querying AWS Organizations resources:

  - accounts
  - organizational units
  - service control policies

``orgcrawler.crawlers.Crawler``
  provides a framework for executing user defined python code in all accounts and regions or a subset thereof.


OrgCrawler also contains two console scripts: ``orgquery`` and ``orgcrawler``.
These attempt to provide a generic interface for running organization queries
and custom crawler functions from the commandline.


See full documentation as https://orgcrawler.readthedocs.io/en/latest/

Currently orgcrawler is tested in python 3.6, 3.7.

'''


setup(
    name='orgcrawler',
    description='Tools for working with AWS Organizations',
    long_description='Tools for working with AWS Organizations',
    long_description_content_type='text/x-rst',
    url='https://github.com/ucopacme/orgcrawler',
    keywords='aws organizations boto3',
    author='Ashley Gould - University of California Office of the President',
    author_email='agould@ucop.edu',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'botocore',
        'boto3',
        'PyYAML',
        'click',
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_namespace_packages(include=['orgcrawler.*']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'orgquery=orgcrawler.cli.orgquery:main',
            'orgcrawler=orgcrawler.cli.orgcrawler:main',
        ],
    },
)
