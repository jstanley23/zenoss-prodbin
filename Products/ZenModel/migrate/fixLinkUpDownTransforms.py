###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2011, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import Migrate

OLD_VERSION =  """
index = None
for key, value in evt.__dict__.items():
   if key.find('1.3.6.1.2.1.2.2.1.1') >= 0:
      index = value
      break
if index is not None:
   for obj in device.os.interfaces.objectItems():
      if obj[1].ifindex == index:
         evt.component = obj[1].id
         break
""".strip()

NEW_VERSION =  """
if_index_str = getattr(evt.details, "ifIndex", None)
if if_index_str is not None:
    if_index = int(if_index_str)
    for interface in device.os.interfaces():
        if interface.ifindex == if_index:
            evt.component = interface.id
            break
""".strip()

class FixLinkUpDownTransforms(Migrate.Step):
    version = Migrate.Version(4, 0, 0)

    def cutover(self, dmd):
        parent = dmd.Events.Net.Link.instances
        event_class_instances = [parent.snmp_linkDown, parent.snmp_linkUp,]
        for event_class_instance in event_class_instances:
            if event_class_instance.transform == OLD_VERSION:
                event_class_instance.transform = NEW_VERSION

FixLinkUpDownTransforms()
