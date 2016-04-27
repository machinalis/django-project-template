# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

VERSION = ''

REQUIREMENTS = parse_requirements('requirements.txt')
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='{{project_name}}',
    version=VERSION,
    description='',
    long_description=README,
    include_package_data=True,
    packages=find_packages('{{project_name}}'),
    install_requires=[str(r.req) for r in requirements],
    entry_points={
        'console_scripts': [
            'manage = {{project_name}}.manage:do_manage',
        ],
    },
)
