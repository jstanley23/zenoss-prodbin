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
if device and evt.eventKey:
    for f in device.os.filesystems():
        if f.name() != evt.component and f.id != evt.component: continue

        # Extract the used blocks from the event's message
        import re
        m = re.search("threshold of [^:]+: current value ([\d\.]+)", evt.message)
        if not m: continue

        # Get the total blocks from the model. Adjust by specified offset.
        totalBlocks = f.totalBlocks * getattr(device, "zFileSystemSizeOffset", 1.0)
        totalBytes = totalBlocks * f.blockSize
        usedBytes = None

        currentValue = float(m.groups()[0])
        if 'usedBlocks' in evt.eventKey:
            usedBytes = currentValue * f.blockSize
        elif 'FreeMegabytes' in evt.eventKey:
            usedBytes = totalBytes - (currentValue * 1048576)
        else:
            continue

        # Calculate the used percent and amount free.
        usedBlocks = float(m.groups()[0])
        p = (usedBytes / totalBytes) * 100
        from Products.ZenUtils.Utils import convToUnits
        free = convToUnits(totalBytes - usedBytes)

        # Make a nicer summary
        evt.summary = "disk space threshold: %3.1f%% used (%s free)" % (p, free)
        evt.message = evt.summary
        break
""".strip()

NEW_VERSION =  """
if device and evt.eventKey:
    for f in device.os.filesystems():
        if f.name() != evt.component and f.id != evt.component: continue

        # Extract the used blocks from the event's message
        import re
        m = re.search("threshold of [^:]+: current value ([\d\.]+)", evt.message)
        if not m: continue

        # Get the total blocks from the model. Adjust by specified offset.
        totalBlocks = f.totalBlocks * getattr(device, "zFileSystemSizeOffset", 1.0)
        totalBytes = totalBlocks * f.blockSize
        usedBytes = None

        currentValue = float(m.groups()[0])
        if 'usedBlocks' in evt.eventKey:
            usedBytes = currentValue * f.blockSize
        elif 'FreeMegabytes' in evt.eventKey:
            usedBytes = totalBytes - (currentValue * 1048576)
        else:
            continue

        try:
            # Calculate the used percent and amount free.
            usedBlocks = float(m.groups()[0])
            p = (usedBytes / totalBytes) * 100
            from Products.ZenUtils.Utils import convToUnits
            free = convToUnits(totalBytes - usedBytes)
            # Make a nicer summary
            evt.summary = "disk space threshold: %3.1f%% used (%s free)" % (p, free)
            evt.message = evt.summary
        except ZeroDivisionError, e:
            # Total size hasn't been calculated
            pass

        break
""".strip()


class FixPerfFilesystemTransform(Migrate.Step):
    version = Migrate.Version(4, 0, 0)

    def cutover(self, dmd):
        if dmd.Events.Perf.Filesystem.transform == OLD_VERSION:
            dmd.Events.Perf.Filesystem.transform = NEW_VERSION


FixPerfFilesystemTransform()

