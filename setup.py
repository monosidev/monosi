# -*- coding: utf-8 -*-

import os
import sys
import pkg_resources
from setuptools import setup, find_packages


path = os.path.abspath('./src')
sys.path.append(path)

VERSION = '0.0.3.post2'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_requires = []
with open(os.path.abspath("requirements.txt"), "r") as f:
    requirements_txt = f.readlines()
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='monosi',
    version=VERSION,
    description='Monosi - Data observability & monitoring toolkit',
    # long_description=readme,
    author='Vocable Inc.',
    author_email='support@monosi.dev',
    url='https://github.com/monosidev/monosi',
    license=license,
    install_requires=install_requires,
    packages=find_packages(
        where="src", 
        include=[
            "agent*",
            "cli*",
            "core*",
            "scheduler*",
            "server*"
        ],
        exclude=["tests"],
    ),
    package_dir={"": "src"},
    entry_points = {
        'console_scripts': [
            'monosi=cli.__main__:main',
        ],
    },
)
