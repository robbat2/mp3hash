# -*- coding: utf-8 -*-

import os

from setuptools import setup

here = os.path.dirname(os.path.realpath(__file__))
readme = os.path.join(here, 'README.rst')

setup(
    name='mp3hash',
    version='0.1',
    description='Music file hasher',
    long_description=open(readme).read(),
    author='Javier Santacruz',
    author_email='javier.santacruz.lc@gmail.com',
    url='http://github.com/jvrsantacruz/mp3hash',
    py_modules=['mp3hash'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    platforms=['Any'],
    scripts=[
        'scripts/mp3hash'
    ]
)
