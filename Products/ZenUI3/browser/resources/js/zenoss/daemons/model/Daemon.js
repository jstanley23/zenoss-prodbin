/*****************************************************************************
 *
 * Copyright (C) Zenoss, Inc. 2013, all rights reserved.
 *
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 *
 ****************************************************************************/
(function(){
    var router = Zenoss.remote.ApplicationRouter;

    Ext.define('Daemons.model.Daemon', {
        extend: 'Ext.data.Model',
        fields: Zenoss.model.BASE_TREE_FIELDS.concat([
            {name: 'id',  type: 'string'},
            {name: 'name',  type: 'string'},
            {name: 'uid',  type: 'string'},
            {name: 'uuid',  type: 'string'},
            {name: 'state',  type: 'boolean',
             convert: function(value, record) {
                 if (value == Daemons.states.UP) return true;
                 if (value == Daemons.states.DOWN) return false;
                 if (value == Daemons.states.STARTING) return false;
                 return null;
             }
            },
            {name: 'autostart',  type: 'boolean'},
            {name: 'isRestarting',  type: 'boolean'},
            {name: 'qtip',  type: 'string'}
        ]),

        proxy: {
            simpleSortMode: true,
            type: 'direct',
            directFn: router.getTree,
            paramOrder: ['uid']
        }
    });

    Ext.define('Daemons.store.Daemons', {
        extend: 'Ext.data.TreeStore',
        model: 'Daemons.model.Daemon',
        nodeParam: 'uid',
        remoteSort: false,
        sorters: {
            direction: 'asc',
            sorterFn: Zenoss.sortTreeNodes
        }
    });

})();
