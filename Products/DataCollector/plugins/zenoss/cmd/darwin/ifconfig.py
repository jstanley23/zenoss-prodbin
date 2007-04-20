###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import re, string

from CollectorPlugin import CommandPlugin

class ifconfig(CommandPlugin):
    """
    ifconfig maps a Darwin ifconfig command to the interfaces relation.
    """
    maptype = "InterfaceMap" 
    command = '/sbin/ifconfig'
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"


    flags = re.compile(".+flags=\d+<(.+)>.+").search


    def condition(self, device, log):
        return device.os.uname == 'Darwin' 


    def chunk(self, output):
        '''splits the ifconfig output into a [] where each item in the list
        represents the ifconfig output for an individual interface'''

        chunks = []
        chunk = []
        for line in output.split('\n'):
            if line.startswith(' '):
                chunk.append(' ')
                chunk.append(line)
            else:
                section = string.join(chunk, ' ').strip()
                if len(section) > 0:
                    chunks.append(section)
                chunk = [line]
        chunks.append(string.join(chunk, ' '))
        return chunks


    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        rm = self.relMap()
        for chunk in self.chunk(results):            
            iface = self.objectMap()
            rm.append(iface)

            intf = chunk.split(':')[0]

            m = self.flags(chunk)
            if m:
                flags = m.groups()[0].split(',')
                if "UP" in flags: iface.operStatus = 1
                else: iface.operStatus = 2
                if "RUNNING" in flags: iface.adminStatus = 1
                else: iface.adminStatus = 2
                
        return rm
