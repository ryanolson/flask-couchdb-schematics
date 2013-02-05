"""
Flask-CouchDB
-------------
Flask-CouchDB provides utilities for using CouchDB with the Flask Web
framework. You can use the direct JSON-document approach, or map documents to
Python objects.
"""

from setuptools import setup

setup(
    name='Flask-CouchDB',
    version='2.0.0dev',
    url='http://bitbucket.org/leafstorm/flask-couchdb/',
    license='MIT',
    description='Provides utilities for using CouchDB with Flask',
    packages=['flask_couchdb'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    dependency_links = [
        'http://github.com/ryanolson/couchdb-python/tarball/master#egg=couchdb-python-2.0.0dev'
    ],
    install_requires=[
        'Flask',
        'couchdb-python>=2.0.0dev'
    ],
    tests_require='nose',
    test_suite='nose.collector',
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
