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

from itertools import imap
from zope.component import adapts
from zope.interface import implements
from Products.Zuul import getFacade
from Products.Zuul.tree import TreeNode
from Products.Zuul.infos import InfoBase, ConfigProperty
from Products.Zuul.interfaces import IServiceInfo
from Products.Zuul.interfaces import IServiceOrganizerNode
from Products.Zuul.interfaces import ICatalogTool, IServiceOrganizerInfo
from Products.ZenModel.ServiceClass import ServiceClass
from Products.ZenModel.ServiceOrganizer import ServiceOrganizer
from Products.ZenModel.Service import Service

class ServiceOrganizerNode(TreeNode):
    implements(IServiceOrganizerNode)
    adapts(ServiceOrganizer)

    @property
    def _evsummary(self):
        return getFacade('service').getEventSummary(self.uid)

    @property
    def text(self):
        text = super(ServiceOrganizerNode, self).text
        count = ICatalogTool(self._object).count((ServiceClass,), self.uid)
        return {'text': text, 'count': count}

    @property
    def children(self):
        cat = ICatalogTool(self._object)
        orgs = cat.search(ServiceOrganizer, paths=(self.uid,), depth=1)
        return imap(ServiceOrganizerNode, orgs)

    @property
    def leaf(self):
        return False


class ServiceInfoBase(InfoBase):

    monitor = ConfigProperty('zMonitor', 'boolean')
    failSeverity = ConfigProperty('zFailSeverity', 'int')

    def getInherited(self):
        return not self._object.hasProperty('zMonitor')

    def setInherited(self, isInherited):
        if isInherited:
            if self._object.hasProperty('zMonitor'):
                self._object.deleteZenProperty('zMonitor')
            if self._object.hasProperty('zFailSeverity'):
                self._object.deleteZenProperty('zFailSeverity')
    isInherited = property(getInherited, setInherited)

class ServiceInfo(ServiceInfoBase):
    implements(IServiceInfo)
    adapts(ServiceClass)

    def getServiceKeys(self):
        return self._object.serviceKeys

    def setServiceKeys(self, value):
        self._object.serviceKeys = value

    serviceKeys = property(getServiceKeys, setServiceKeys)

    def getPort(self):
        return self._object.port

    def setPort(self, value):
        self._object.port = value

    port = property(getPort, setPort)

    @property
    def count(self):
        numInstances = ICatalogTool(self._object).count(
            (Service,), self.uid)

        return numInstances

class ServiceOrganizerInfo(ServiceInfoBase):
    implements(IServiceOrganizerInfo)
    adapts(ServiceOrganizer)
