#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Django notifications rest setup file for pip package '''
import ast
import re
import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=no-name-in-module,import-error

_version_re = re.compile(r'__version__\s+=\s+(.*)')  # pylint: disable=invalid-name

with open('notifications_rest/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(  # pylint: disable=invalid-name
        f.read().decode('utf-8')).group(1)))

setup(
    name='django-notifications-rest',
    version=version,
    description='A django notifications package exposed through API Rest',
    long_description=open('README.md').read(),
    author='Yusniel Hidalgo Delgado',
    author_email='yhidalgo86@gmail.com',
    url='https://github.com/yhdelgado/django-notifications-rest',
    include_package_data=True,
    long_description_content_type="text/markdown",
    exclude_package_data={
        '': ['djangotools', 'django_notifications_rest.egg-info']
    },
    packages=setuptools.find_packages(exclude=['djangotools']),
    python_requires=">=3.5",
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ],
    keywords='django notifications github rest api',
    license='MIT',
)
