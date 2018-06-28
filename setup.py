#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
from pyarborsp import __version__


setup(
    name="pyArborSP",
    version=__version__,
    description="API client for interacting with Arbor Networks SP product",
    long_description="API client for interacting with Arbor Networks SP product",
    url="https://github.com/pyArborSP",
    packages=find_packages(exclude=['docs','tests']),
    author="James Williams",
    author_email="james.williams@rackspace.com",
    keywords="pyArborSP",
    python_requires=">3.6",
    install_requires=[
        "requests==2.19.1",
    ],
)