# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='metatype',
    version='0.1.1.2',
    description='Implementation of base dict types for metaformat versions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wefindx/metatype',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'metawiki',
        'typology',
        'gpgrecord',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
        ],
    }
)
