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

__all__ = ['CouchDBManager']


### The manager class

class CouchDBManager(object):
    """
    This manages connecting to the database every request and synchronizing
    the view definitions to it.
    
    :param auto_sync: Whether to automatically sync the database every
                      request. (Defaults to `True`.)
    """
    def __init__(self, app=None, auto_sync=True):
        self.auto_sync = auto_sync
        self.dc_viewdefs = {}
        self.general_viewdefs = []
        self.sync_callbacks = []
        self.server_url = None
        self.db_name = None
        self.server = None
        self._db = None
        self.is_setup = False
        self.app = app
        if self.app is not None:
           self.init_app(app)
    
    def all_viewdefs(self):
        """
        This iterates through all the view definitions registered generally
        and the ones on specific document classes.
        """
        return itertools.chain(self.general_viewdefs,
                               *self.dc_viewdefs.itervalues())
    
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
            self.dc_viewdefs[dc] = viewdefs
    
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
        return self._db_for_app(app)
    
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
        db = self._db_for_app(app)

        CouchDBViewDefinition.sync_many(
            db, tuple(self.all_viewdefs()),
            callback=getattr(self, 'update_design_doc', None)
        )
        for callback in self.sync_callbacks:
            callback(db)

    def _db_for_app(self,app):
        """
        If app has a different server/db configuration than what was used in
        setup, the database will be setup on the requested server.

        If not, the default database will be used, thus avoiding unnecessary
        HEAD transactions to the couchdb server.
        """
        assert self._db is not None
        server_url = self.server_url
        db_name = self.db_name
        server = self.server
        db = self._db
        update_db = False

        if app is not None:
           server_url = app.config['COUCHDB_SERVER']
           db_name = app.config['COUCHDB_DATABASE']

        if server_url != self.server_url:
           server = couchdb.Server(server_url)
           update_db = True

        if db_name != self.db_name or update_db:
           db = self.get_or_create_db(db_name, server)

        return db

    def get_or_create_db(self, db_name, server=None):
        server = server or self.server
        if db_name not in server:
           db = server.create(db_name)
        else:
           db = server[db_name]
        return db

    def setup(self, app):
        """
        This method sets up the request/response handlers needed to connect to
        the database on every request.
        
        :param app: The application to set up.
        """

        self.server_url = app.config.get('COUCHDB_SERVER','http://localhost:5984/')
        self.db_name = app.config.get('COUCHDB_DATABASE', app.name.lower())
        self.server = couchdb.Server(self.server_url)
        self._db = self.get_or_create_db(self.db_name)
        

    def init_app(self, app):
        app.before_request(self.request_start)
        #pp.after_request(self.request_end)

    def request_start(self):
        if self.is_setup and self.auto_sync and not current_app.config.get('DISABLE_AUTO_SYNC'):
            self.sync(current_app)
        #g.couch = self.connect_db(current_app)
        g.couch = self
    
    def request_end(self, response):
        del g.couch
        return response

    @property
    def db(self):
        ctx = stack.top
        if ctx is not None:
           if not hasattr(ctx, 'couch'):
              self.setup(current_app)
              self.sync(current_app)
              ctx.couch = self 
           return ctx.couch.connect_db()
