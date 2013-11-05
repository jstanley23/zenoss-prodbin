##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging

from Products import Zuul
from Products.ZenMessaging.audit import audit
from Products.ZenUtils.Ext import DirectResponse
from Products.Zuul.interfaces import IInfo, ITreeNode
from Products.Zuul.routers import TreeRouter


log = logging.getLogger('zen.MonitorRouter')


class MonitorRouter(TreeRouter):
    """
    """

    def _getFacade(self):
        return Zuul.getFacade('monitors', self.context)

    def getTree(self, id):
        """
        Returns the tree structure of the application (service) hierarchy where
        the root node is the organizer identified by the id parameter.

        @type  id: string
        @param id: Id of the root node of the tree to be returned
        @rtype:   [dictionary]
        @return:  Object representing the tree
        """
        facade = self._getFacade()
        monitors = facade.queryPerformanceMonitors()
        nodes = map(ITreeNode, monitors)
        data = Zuul.marshal(nodes)
        return data

    def getInfo(self, id):
        """
        Returns the serialized info object for the given id
        @type: id: String
        @param id: Valid id of a application
        @rtype: DirectResponse
        @return: DirectResponse with data of the application
        """
        facade = self._getFacade()
        monitor = facade.get(id)
        data = Zuul.marshal(ITreeNode(monitor))
        return DirectResponse.succeed(data=data)
