Flask-CouchDB-Schematics
========================

This library helps you use CouchDB & Schmatics with Flask.

forked from: https://bitbucket.org/leafstorm/flask-couchdb @ revision
3d5855f

The semantics of intializing a document as changed to match the
schematics models. Rather than accepting keyword arguments, the
constructor now wants the data for the model in a single dictionary.

.. code:: python

    from flask.ext.couchdb.document import Document

    doc = Document({"key"; "value"))

For more info on Flask extensions, see:
http://flask.pocoo.org/docs/extensiondev/
