###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
import time

from Products.ZenUI3.browser.eventconsole.grid import column_config
from Products.ZenUtils.Ext import DirectRouter
from Products.Zuul import getFacade
from Products.Zuul.decorators import require
from Products import Zuul

class EventsRouter(DirectRouter):

    def __init__(self, context, request):
        super(EventsRouter, self).__init__(context, request)
        self.api = getFacade('event')

    def query(self, limit=None, start=None, sort=None, dir=None, params=None,
              history=False, uid=None, criteria=()):
        if uid is None:
            uid = self.context
        events = self.api.query(limit, start, sort, dir, params, uid, criteria,
                               history)
        self._set_asof(time.time())
        disabled = not Zuul.checkPermission('Manage Events')
        return {'events':events['data'], 
                'disabled': disabled, 
                'totalCount': events['total'] }

    def queryHistory(self, limit, start, sort, dir, params):
        return self.query(limit, start, sort, dir, params, history=True)

    @require('Manage Events')
    def acknowledge(self, evids=None, ranges=None, start=None, limit=None,
                    field=None, direction=None, params=None, history=False,
                    uid=None):
        if uid is None:
            uid = self.context
        self.api.acknowledge(evids, ranges, start, limit, field, direction,
                             params, asof=self._asof, context=uid,
                             history=history)
        return {'success':True}

    @require('Manage Events')
    def unacknowledge(self, evids=None, ranges=None, start=None, limit=None,
                      field=None, direction=None, params=None, history=False,
                      uid=None):
        if uid is None:
            uid = self.context
        self.api.unacknowledge(evids, ranges, start, limit, field, direction,
                               params, asof=self._asof, context=uid,
                               history=history)
        return {'success':True}

    @require('Manage Events')
    def reopen(self, evids=None, ranges=None, start=None, limit=None,
               field=None, direction=None, params=None, history=True,
               uid=None):
        if uid is None:
            uid = self.context
        self.api.reopen(evids, ranges, start, limit, field, direction, params,
                        asof=self._asof, context=uid, history=history)
        return {'success':True}

    @require('Manage Events')
    def close(self, evids=None, ranges=None, start=None, limit=None,
              field=None, direction=None, params=None, history=False, uid=None):
        if uid is None:
            uid = self.context
        self.api.close(evids, ranges, start, limit, field, direction, params,
                        asof=self._asof, context=uid, history=history)
        return {'success':True}


    def state_ranges(self, state=1, field='severity', direction='DESC',
                     params=None, history=False, uid=None):
        if uid is None:
            uid = self.context
        return self.api.getStateRanges(state, field, direction, params, history,
                                       uid, self._asof);


    def detail(self, evid, history=False):
        event = self.api.detail(evid, history)
        if event:
            return { 'event': [event] }

    @require('Manage Events')
    def write_log(self, evid=None, message=None, history=False):
        self.api.log(evid, message, history)

    @require('Manage Events')
    def classify(self, evids, evclass, history=False):
        zem = self.api._event_manager(history)
        msg, url = zem.manage_createEventMap(evclass, evids)
        if url:
            msg += "<br/><br/><a href='%s'>Go to the new mapping.</a>" % url
        return {'success':bool(url), 'msg': msg}

    @require('Manage Events')
    def add_event(self, summary, device, component, severity, evclasskey, evclass):
        evid = self.api.create(summary, severity, device, component,
                               eventClassKey=evclasskey, eventClass=evclass)
        return {'success':True, 'evid':evid}

    def column_config(self, uid=None):
        if uid==None:
            uid = self.context
        return column_config(self.api.fields(uid), self.request)

