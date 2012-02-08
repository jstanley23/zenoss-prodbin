###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2011 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = '''NullConfig

Provides a blank configuration to send no proxies to the remote
collector.
'''

from Products.ZenCollector.services.config import NullConfigService

class NullConfig(NullConfigService):
    pass