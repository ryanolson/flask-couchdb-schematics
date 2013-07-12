# -*- coding: utf-8 -*-

from flask import json
from couchdb.client import ViewResults, Row
from couchdb.design import ViewDefinition as CouchDBViewDefinition

### Pagination

class Page(object):
    """
    This represents a single page of items. They are created by the `paginate`
    function.
    """
    #: A list of the actual items returned from the view.
    items = ()
    
    #: The `start` value for the next page, if there is one. If not, this
    #: is `None`. It is JSON-encoded, but not URL-encoded.
    next = None
    
    #: The `start` value for the previous page, if there is one. If not,
    #: this is `None`.
    prev = None
    
    def __init__(self, items, next=None, prev=None):
        self.items = items
        self.next = next
        self.prev = prev


def _clone(results, **options):
    """
    This clones a `ViewResults` object. It's mostly for use by the `paginate`
    function.
    """
    newopts = results.options.copy()
    newopts.update(options)
    return ViewResults(results.view, newopts)


def paginate(view, count, start=None):
    """
    This implements linked-list pagination. You pass in the view to use, the
    number of items per page, and the JSON-encoded `start` value for the page,
    and it will return a `Page` instance.
    
    Since this is "linked-list" style pagination, it only allows direct
    navigation using next and previous links. However, it is also very fast
    and efficient.
    
    You should probably use the `start` values as a query parameter (e.g.
    ``?start=whatever``).
    
    :param view: A `ViewResults` instance. (You get this by calling, slicing,
                 or subscripting a `ViewDefinition` or `ViewField`.)
    :param count: The number of items to put on a single page.
    :param start: The start value of the page, as a string.
    """
    # first, patch the wrapper
    if isinstance(view, CouchDBViewDefinition):
        view = view()
    old_wrapper = view.view.wrapper or (lambda r: r)
    view.view.wrapper = Row
    rewrap = lambda r: [old_wrapper(i) for i in r]
    
    # then, actually paginate
    # the algorithm we're using is in the misc/pagination-algorithm.txt file
    if start is None:
        # first page
        results = list(_clone(view, limit=count + 1))
        if len(results) <= count:
            # only one page
            return Page(rewrap(results), None, None)
        else:
            nextstart = results[-1]
            next = json.dumps([nextstart.key, nextstart.id])
            return Page(rewrap(results[:-1]), next, None)
    else:
        # subsequent page
        descending = view.options.get('descending', False)
        try:
            startkey, startid = json.loads(start)
        except ValueError:
            abort(400)
        forwards = list(_clone(view, limit=count + 1, startkey=startkey,
                               startkey_docid=startid))
        backwards = list(_clone(view, limit=count, startkey=startkey,
                                startkey_docid=startid, skip=1,
                                descending=not descending))
        
        # processing "next" link
        if len(forwards) <= count:
            # there isn't a next page
            next = None
            items = forwards
        else:
            # there is a next page
            nextstart = forwards[-1]
            next = json.dumps([nextstart.key, nextstart.id])
            items = forwards[:-1]
        
        # processing "previous" link
        if not backwards:
            # no previous results
            prev = None
        else:
            prevstart = backwards[-1]
            prev = json.dumps([prevstart.key, prevstart.id])
        
        return Page(rewrap(items), next, prev)
