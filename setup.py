# YOU NEED TO EDIT THESE
AUTHOR = 'Ben Gillies'
AUTHOR_EMAIL = 'bengillies@gmail.com'
NAME = 'tiddlywebplugins.csv'
DESCRIPTION = 'A csv serializer for TiddlyWeb'
VERSION = '0.5'


import os

from setuptools import setup, find_packages


# You should carefully review the below (install_requires especially).
setup(
    namespace_packages = ['tiddlywebplugins'],
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'http://pypi.python.org/pypi/%s' % NAME,
    platforms = 'Posix; MacOS X; Windows',
    packages = find_packages(exclude=['test']),
    install_requires = ['setuptools', 'tiddlyweb'],
    zip_safe = False
    )
