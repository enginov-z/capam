//model
odoo.define('rea_management.HistModel', function (require) {
    'use strict';
    var AbstractModel = require('web.AbstractModel');
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;
    var HistModel = AbstractModel.extend({

        //-----------------------------------------------------------------------------------
        //Public
        //----------------------------------------------------------------------------------
        init: function () {
            this._super.apply(this, arguments);
            this.data = {};

        },
        get: function () {
            return this.data;
        },
        load: function (params) {
            this.data.count = 0;
            this.data.offset = 0;
            this.data.limit = 80;
            this.partnerToCache = [];
            this.partnerIds = [];
            this.resPartnerField = params.resPartnerField;
            this.model = params.modelName;
            this.context = params.context;
            this.fields = params.fieldNames;
            this.domain = params.domain;
            this.params = params;
            this.orderBy = params.orderBy;
            this.routing = params.routing;
            this.numberOfLocatedRecords = 0;
            return this._fetchData();
        },
        _fetchData: async function () {
            //case of empty map
            if (!this.resPartnerField) {
                this.data.records = [];
                this.data.route = { routes: [] };
                return;
            }
            var results = await this._fetchRecordData();
            this.data.records = results.records;
            this.data.count = results.length;
            this.partnerIds = [];
            if (this.model === "res.partner" && this.resPartnerField === "id") {
                this.data.records.forEach((record) => {
                    this.partnerIds.push(record.id);
                    record.partner_id = [record.id];
                });
            } else {
                this._fillPartnerIds(this.data.records);
            }

            this.partnerIds = _.uniq(this.partnerIds);
            return this._partnerFetching(this.partnerIds);
        },
        _partnerFetching: async function (partnerIds) {
            this.data.partners = partnerIds.length ? await this._fetchRecordsPartner(partnerIds) : [];
            
        },
        _fillPartnerIds: function (records) {
            return records.forEach((record) => {
                if (record[this.resPartnerField]) {
                    this.partnerIds.push(record[this.resPartnerField][0]);
                }
            });
        },
        _fetchRecordsPartner: function (ids) {
            return this._rpc({
                model: 'res.company',
                method: 'search_read',
                fields: ['contact_address_complete', 'partner_latitude', 'partner_longitude'],
                domain: [['contact_address_complete', '!=', 'False'], ['id', 'in', ids]],
            });
        },
        _fetchRecordData: function () {
            return this._rpc({
                route: '/web/dataset/search_read',
                model: this.model,
                context: this.context,
                fields: this.fields,
                domain: this.domain,
                orderBy: this.orderBy,
                limit: this.data.limit,
                offset: this.data.offset
            });
        },
    })
        
        return HistModel;
});

//render
odoo.define('rea_management.HistRenderer', function (require) {
    "use strict";
    var core = require('web.core');
    var AbstractRenderer = require('web.AbstractRenderer');
    var field_utils = require('web.field_utils');
    var qweb = core.qweb;

    var MapRenderer = AbstractRenderer.extend({
        className: "container-fluid",
        //---------------------------------------------------------------------------
        //Public
        //--------------------------------------------------------------------------

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.hasFormView = params.hasFormView;
            this.defaultOrder = params.defaultOrder;

            this.isInDom = false;
            this.mapIsInit = false;
            this.markers = [];
            this.polylines = [];


        },
        on_attach_callback: function () {
            this.isInDom = true;
            

        },

        /*
        *called each time the renderer is detached from the DOM.
        */
        on_detach_callback: function () {
            this.isInDom = false;
        },
                destroy: function () {
           
           
            return this._super.apply(this, arguments);
        },
    _addInter: function () {
                var l = []
var g=""
            this.$pinList = $(qweb.render('HistView.main'), { g: g });
            var $container = this.$el.find('.container');
            if ($container.length) {
                $container.replaceWith(this.$pinList);
            } else {
                this.$el.append(this.$pinList);
            }

            
        },

    _render: function () {
            this._addInter();
            return Promise.resolve();
        }
    });
    return MapRenderer;
});

//the view
odoo.define('rea_management.HistView', function (require) {
    "use strict";

    var HistModel = require('rea_management.HistModel');
   // var HistController = require('rea_management.HistController');
    var HistRenderer = require('rea_management.HistRenderer');
    var AbstractView = require('web.AbstractView');
    var viewRegistry = require('web.view_registry');
    var _t = require('web.core')._t;

    var HistView = AbstractView.extend({
        jsLibs: [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js',
          
        ],
        config: _.extend({}, AbstractView.prototype.config, {
            Model: HistModel,
           // Controller: HistController,
            Renderer: HistRenderer,
        }),
        icon: 'fa-flag',
        display_name: 'Histogramme',
        viewType: 'hist',
        mobile_friendly: true,
        searchMenuTypes: [],

        init: function (viewInfo, params) {
            this._super.apply(this, arguments);

            var fieldNames = [];
            var fieldNamesMarkerPopup = [];

            

           

            this.loadParams.routing = this.arch.attrs.routing ? true : false;
            this.rendererParams.numbering = this.arch.attrs.routing ? true: false;
            this.rendererParams.defaultOrder = this.arch.attrs.default_order;
            this.rendererParams.panelTitle = this.arch.attrs.panel_title || params.displayName || _t('Items');

           


            this.rendererParams.hasFormView = params.actionViews.find(function (view) {
                return view.type === "form";
            });
        },
    });
    viewRegistry.add('hist', HistView);
    return HistView;
});
