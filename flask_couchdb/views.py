# -*- coding: utf-8 -*-

from couchdb.design import ViewDefinition as CouchDBViewDefinition
from couchdb.old_mapping import ViewField as CouchDBViewField
from flask import g

class ViewDefinition(CouchDBViewDefinition):
    def __call__(self, db=None, **options):
        """
        This executes the view with the given database. If a database is not
        given, the thread-local database (``g.couch``) is used.
        
        :param db: The database to use, if necessary.
        :param options: Options to pass to the view.
        """
        return super(ViewDefinition, self).__call__(db or g.couch, **options)
#       return CouchDBViewDefinition.__call__(self, db or g.couch, **options)
    
    def __getitem__(self, item):
        """
        Since it's possible to use this variant of `ViewDefinition` without
        an explicit database, this method is added for simplicity. For
        example, both sets of calls are equivalent::
        
            viewdef()['spam']
            viewdef['spam']
            
            viewdef()['eggs':'ham']
            viewdef['eggs':'ham']
        
        :param item: An item, or a slice.
        """
        return self()[item]


# only overridden so it will use our ViewDefinition
# this should be transparent to the user

class ViewField(CouchDBViewField):
    def __get__(self, instance, cls=None):
        wrapper = super(ViewField, self).__get__(instance, cls).wrapper
        return ViewDefinition(self.design, self.name, self.map_fun,
                              self.reduce_fun, language=self.language,
                              wrapper=wrapper, **self.defaults)


