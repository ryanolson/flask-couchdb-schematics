# -*- coding: utf-8 -*-


import couchdb
import couchdb.mapping as mapping

from flask import g

from schematics.models import Model
from schematics.types.base import *
from schematics.types.compound import *
from schematics.serialize import *
from schematics.validation import validate_instance, validate_instance as validate_document

from schematics.types.base import __all__ as base_all
from schematics.types.compound import __all__ as compound_all
from schematics.serialize import __all__ as serialize_all


__all__ = ["Document", "Model", "validate_instance", "validate_document"]
__all__.extend(base_all)
__all__.extend(compound_all)
__all__.extend(serialize_all)

class Document(mapping.Document):

    @classmethod
    def load(cls, id, db=None, **kwargs):
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
        return super(Document, cls).load(db or g.couch, id, **kwargs)
    
    def store(self, db=None, validate=True):
        """
        This saves the document to the database. If a database is not given,
        the thread-local database (``g.couch``) is used.
        
        :param db: The database to use. Optional.
        """
        return mapping.Document.store(self, db or g.couch, validate)

