/*****************************************************************************
 *
 * Copyright (C) Zenoss, Inc. 2011, all rights reserved.
 *
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 *
 ****************************************************************************/


(function(){

    Ext.define("Zenoss.ComponentTemplatePanel", {
        alias:['widget.componenttemplatepanel'],
        extend:"Ext.Panel",
        constructor: function(config) {
            config = config || {};
            Ext.applyIf(config, {
                layout: 'border',
                defaults: {
                    split: true
                },
                items:[{
                    region: 'center',
                    width: '65%',
                    xtype: 'DataSourceTreeGrid',
                    ref: 'dataSourceTreeGrid',
                    title: null,
                    tbarItems:[{
                        xtype: 'tbtext',
                        text: _t('Data Sources')
                    }, '-'],
                    dsAddHandler: function() {
                        var templateUid = this.ownerCt.ownerCt.ownerCt.getContext();
                        if (!templateUid) {
                            new Zenoss.dialog.ErrorDialog({message: _t('There is no template to which to add a datasource.')});
                            return;
                        }
                        Ext.create('Zenoss.templates.AddDataSourceDialog', {templateUid: templateUid}).show();
                    },
                    dpAddHandler: function() {
                        var selectedNode = this.ownerCt.ownerButton.ownerCt.ownerCt.getSelectionModel().getSelectedNode();
                        if (!selectedNode) {
                            new Zenoss.dialog.ErrorDialog({message: _t('You must select a data source.')});
                            return;
                        }
                        Ext.create('Zenoss.templates.AddDataPointDialog', {
                            dataSourceUid: selectedNode.data.uid,
                            dataSourceId: selectedNode.data.id
                        }).show();
                    },
                    root: {
                        uid: config.contextUid
                    }
                },{
                    xtype: 'panel',
                    layout: 'border',
                    region: 'east',
                    width: '35%',
                    defaults: {
                        split: true
                    },
                    items:[{
                        id: 'component_template_threshold',
                        region: 'north',
                        height: '50%',
                        title: null,
                        stateId: 'component_template_thresholds',
                        xtype: 'thresholddatagrid',
                        ref: '../thresholds',
                        getTemplateUid: function() {
                            return this.getContext();
                        },
                        tbarItems:[{
                            xtype: 'tbtext',
                            text: _t('Thresholds')
                        }, '-']
                    }, {
                        xtype: 'graphgrid',
                        ref: '../graphGrid',
                        height: '50%',
                        region: 'center',
                        title: null,
                        tbarItems:[{
                            xtype: 'tbtext',
                            text: _t('Graph Definitions')
                        }, '-'],
                        getSelectedTemplateUid: function() {
                            return this.uid;
                        }
                    }]
                }]
            });
            this.callParent(arguments);
        },
        setContext: function(uid) {
            this.uid = uid;
            this.dataSourceTreeGrid.setContext(uid);
            this.thresholds.setContext(uid);
            this.graphGrid.setContext(uid);
        },
        getContext: function() {
            return this.uid;
        }
    });

})();
