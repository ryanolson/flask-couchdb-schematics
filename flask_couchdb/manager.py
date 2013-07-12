# -*- coding: utf-8 -*-
"""

flask_couchdb.manager
~~~~~~~~~~~~~~~~~~~~~

This package provides utilities to make using Flask with a 
CouchDB database server easier.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see LICENSE for details

"""

import itertools
import couchdb
from couchdb.design import ViewDefinition as CouchDBViewDefinition
from flask import g, current_app
from flask import _app_ctx_stack as stack

__all__ = ['CouchDB']


### The manager class

class CouchDB(object):
    """
    This manages connecting to the database every request and synchronizing
    the view definitions to it.
    
    :param auto_sync: Whether to automatically sync the database every
                      request. (Defaults to `False`.)
    """
    def __init__(self, app=None, server=None, db=None):
        self.doc_viewdefs = {}
        self.general_viewdefs = []
        self.sync_callbacks = []
        self.db = db
        self.server = server
        self.app = app
        if self.app is not None:
           self.init_app(app)
    
    def init_app(self, app):
        app.before_request(self.request_start)

    def request_start(self):
        g.couch = self

    def all_viewdefs(self):
        """
        This iterates through all the view definitions registered generally
        and the ones on specific document classes.
        """
        return itertools.chain(self.general_viewdefs,
                               *self.doc_viewdefs.itervalues())
    
    def add_document(self, dc):
        """
        This adds all the view definitions from a document class so they will
        be added to the database when it is synced.
        
        :param dc: The class to add. It should be a subclass of `Document`.
        """
        viewdefs = []
        for name in dir(dc):
            item = getattr(dc, name)
            if isinstance(item, CouchDBViewDefinition):
                viewdefs.append(item)
        if viewdefs:
            self.doc_viewdefs[dc] = viewdefs
    
    def add_viewdef(self, viewdef):
        """
        This adds standalone view definitions (it should be a `ViewDefinition`
        instance or list thereof) to the manager. It will be added to the
        design document when it it is synced.
        
        :param viewdef: The view definition to add. It can also be a tuple or
                        list.
        """
        if isinstance(viewdef, CouchDBViewDefinition):
            self.general_viewdefs.append(viewdef)
        else:
            self.general_viewdefs.extend(viewdef)
    
    def on_sync(self, fn):
        """
        This adds a callback to run when the database is synced. The callbacks
        are passed the live database (so they should use that instead of
        relying on the thread locals), and can do pretty much whatever they
        want. The design documents have already been synchronized. Callbacks
        are called in the order they are added, but you shouldn't rely on
        that.
        
        If you can reliably detect whether it is necessary, this may be a good
        place to add default data. However, the callbacks could theoretically
        be run on every request, so it is a bad idea to insert the default
        data every time.
        
        :param fn: The callback function to add.
        """
        self.sync_callbacks.append(fn)
    
    def connect_db(self, app=None):
        """
        This connects to the database for the given app. It presupposes that
        the database has already been synced, and as such an error will be
        raised if the database does not exist.
        
        :param app: The app to get the settings from.
        """
        if self.db: return self.db
        self.server = couchdb.Server( app.config['COUCHDB_SERVER'] )
        self.db = self.server[ app.config['COUCHDB_DATABASE'] ]
        return self.db
    
    def sync(self, app=None):
        """
        This syncs the database for the given app. It will first make sure the
        database exists, then synchronize all the views and run all the
        callbacks with the connected database.
        
        It will run any callbacks registered with `on_sync`, and when the
        views are being synchronized, if a method called `update_design_doc`
        exists on the manager, it will be called before every design document
        is updated.
        
        :param app: The application to synchronize with.
        """
        db = self.db
        CouchDBViewDefinition.sync_many(
            db, tuple(self.all_viewdefs()),
            callback=getattr(self, 'update_design_doc', None)
        )
        for callback in self.sync_callbacks:
            callback(db)

