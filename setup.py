"""
Flask-CouchDB
-------------
Flask-CouchDB provides utilities for using CouchDB with the Flask Web
framework. You can use the direct JSON-document approach, or map documents to
Python objects.
"""

from setuptools import setup

test_requirements=[
    'pytest'
]

setup(
    name='Flask-CouchDB-Schematics',
    version='1.0.0',
    author="Ryan Olson",
    author_email="rmolson@gmail.com",
    url='http://github.com/ryanolson/flask-couchdb-schematics/',
    license='MIT',
    description='Provides utilities for using CouchDB + Schematics with Flask',
    packages=['flask_couchdb'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'couchdb-schematics'
    ] + test_requirements,
    dependency_links = [
    ],
    tests_require = test_requirements,
)
