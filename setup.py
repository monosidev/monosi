# -*- coding: utf-8 -*-

from os import path
import pkg_resources
from setuptools import setup, find_namespace_packages

VERSION = '0.0.2.post3'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_requires = []
with open(path.abspath("requirements.txt"), "r") as f:
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
    packages=find_namespace_packages(include=['monosi', 'monosi.*'], exclude=('tests', 'docs')),
    entry_points = {
        'console_scripts': [
            'monosi=monosi.__main__:main',
        ],
    },
)
