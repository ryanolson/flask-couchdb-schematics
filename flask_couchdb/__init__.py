# -*- coding: utf-8 -*-
"""

flask_couchdb
~~~~~~~~~~~~~

This package provides utilities to make using Flask with a 
CouchDB database server easier.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see LICENSE for details

"""

from flask_couchdb.manager import CouchDB
from flask_couchdb.views import ViewDefinition, ViewField
from flask_couchdb.pagination import Page, Row, paginate 
from flask_couchdb.document import *
from flask_couchdb.document import __all__ as document_all
import flask_couchdb.schematics_document as schematics_document

__all__ = ['CouchDB', 'ViewDefinition', 'ViewField', 'Row', 'paginate', 'schematics_document']
__all__.extend( document_all )


version_info = ('0', '1', '0', 'beta')
__version__ = '{}.{}.{}-{}'.format(*version_info)
