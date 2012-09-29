#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

setup(
    name='vecc',
    version=__import__('vecc').__version__,
    author='Mathieu Agopian',
    author_email='mathieu.agopian@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/magopian/vecc',
    license='BSD',
    description='Video Embed Code Cleaner',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
            vecc = vecc.vecc:main"""
)
