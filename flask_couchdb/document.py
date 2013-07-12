# -*- coding: utf-8 -*-

from flask import g
from couchdb.mapping import (Field, TextField, FloatField, IntegerField,
                             LongField, BooleanField, DecimalField, DateField,
                             DateTimeField, TimeField, DictField, ListField,
                             Mapping, DEFAULT)
import couchdb
import couchdb.mapping as mapping

__all__ = ["Document"]
mapping.__all__.remove('ViewField')
__all__.extend(mapping.__all__)

class Document(mapping.Document):
    """
    This class can be used to represent a single "type" of document. You can
    use this to more conveniently represent a JSON structure as a Python
    object in the style of an object-relational mapper.
    
    You populate a class with instances of `Field` for all the attributes you
    want to use on the class. In addition, if you set the `doc_type`
    attribute on the class, every document will have a `doc_type` field
    automatically attached to it with that value. That way, you can tell
    different document types apart in views.
    """
    def __init__(self, *args, **kwargs):
        mapping.Document.__init__(self, *args, **kwargs)
        cls = type(self)
        if hasattr(cls, 'doc_type'):
            self._data['doc_type'] = cls.doc_type
    
    @classmethod
    def load(cls, id, db=None):
        """
        This is used to retrieve a specific document from the database. If a
        database is not given, the thread-local database (``g.couch``) is
        used. 
        
        For compatibility with code used to the parameter ordering used in the
        original CouchDB library, the parameters can be given in reverse
        order.
        
        :param id: The document ID to load.
        :param db: The database to use. Optional.
        """
        if isinstance(id, couchdb.Database):
            id, db = db, id
        return super(Document, cls).load(db or g.couch.db, id)
    
    def store(self, db=None):
        """
        This saves the document to the database. If a database is not given,
        the thread-local database (``g.couch``) is used.
        
        :param db: The database to use. Optional.
        """
        return mapping.Document.store(self, db or g.couch.db)

