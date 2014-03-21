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
    version='0.1.0-beta',
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
