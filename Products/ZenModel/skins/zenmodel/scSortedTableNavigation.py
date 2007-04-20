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
## Script (Python) "sortedTableNavigation"
##parameters=tableName,totalLen,batch
##bind context=context
##title=Build the navigation bar at the bottom of a sorted table

request=context.REQUEST
session=request.SESSION
if session.has_key(tableName):
    sortedTableState = session[tableName]
    start = sortedTableState['start']
    navbar = ""
    if start != 0 and totalLen:
        navbar +=("""<a href="%s?tableName=%s&start:int=%d">First</a>&nbsp;\n"""
                % (request.URL, tableName, 0))
        navbar +=(
            """<a href="%s?tableName=%s&start:int=%d">Previous</a>&nbsp;\n"""
                % (request.URL, tableName, batch.previous.first))
    else:
        navbar += "First &nbsp; Previous &nbsp;"
    navbar += """<select class="tableheader" name=navurl"""
    navbar += " onchange=\"document.location.href=this"
    navbar += "[this.selectedIndex].value\">\n"
    lastindex=0
    for index in range(0, totalLen, batch.size):
        pagenumber = 1+index/batch.size
        if start != index:
            navbar +=("""<option value="%s?tableName=%s&start:int=%d">%d"""
                        % (request.URL, tableName, index, pagenumber))
        else:
            navbar +=("""<option value="%s?tableName=%s&start:int=%d" selected>%d"""
                        % (request.URL, tableName, index, pagenumber))
        navbar += """</option>\n"""
        lastindex=index
                                        
    navbar += """</select> &nbsp;"""
    if batch.next:
        navbar +=("""<a href="%s?tableName=%s&start:int=%d">Next</a>&nbsp;\n""" 
                % (request.URL, tableName, batch.next.first))
        navbar +=("""<a href="%s?tableName=%s&start:int=%d">Last</a>&nbsp;\n""" 
                % (request.URL, tableName, lastindex))
    else:
        navbar += "Next &nbsp; Last"
    return navbar + "\n"
else:
    raise "SortedTableSessionError", \
            "Can't find %s tableinfo in session" % tableName
