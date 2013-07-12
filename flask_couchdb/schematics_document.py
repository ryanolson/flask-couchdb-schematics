# -*- coding: utf-8 -*-


import couchdb
from couchdb_schematics.document import SchematicsDocument

from flask import g

from schematics.models import Model, ModelMeta
from schematics.types.base import *
from schematics.types.compound import *

#from schematics.types.base import __all__ as base_all
#from schematics.types.compound import __all__ as compound_all

__all__ = ["Document", "Model"]
#__all__.extend(base_all)
#__all__.extend(compound_all)

class Document(SchematicsDocument):

    @classmethod
    def load(cls, id, db=None, **kwargs):
        """
        This is used to retrieve a specific document from the database. If a
        database is not given, the thread-local database (``g.couch.db``) is
        used. 
        
        For compatibility with code used to the parameter ordering used in the
        original CouchDB library, the parameters can be given in reverse
        order.
        
        :param id: The document ID to load.
        :param db: The database to use. Optional.
        """
        if isinstance(id, couchdb.Database):
            id, db = db, id
        return super(Document, cls).load(db or g.couch.db, id, **kwargs)
    
    def store(self, db=None, validate=True):
        """
        This saves the document to the database. If a database is not given,
        the thread-local database (``g.couch.db``) is used.
        
        :param db: The database to use. Optional.
        """
        return super(Document,self).store(db or g.couch.db, validate)

