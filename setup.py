from setuptools import setup, find_packages
import sys
import os

# Python 3 conversion
extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

requires = ['distribute', 'flask', 'gunicorn']
description = "A python URL shortener using flask/gunicorn"

if os.path.exists('README.md'):
    f = open('README.md')
    try:
        long_description = f.read()
    finally:
        f.close()
else:
    long_description = description

setup(
    name='Stubby',
    version='0.1',
    description=description,
    long_description=long_description,
    author='Philip Jackson',
    author_email='pjackson@softlayer.com',
    packages=find_packages(),
    license='The BSD License',
    zip_safe=False,
    url='https://github.com/underscorephil/stubby/tree/blueprint',
    install_requires=requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    **extra
)
