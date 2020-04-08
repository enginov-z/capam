odoo.define('map_controller_custom',function(require){
    var core = require('web.core');
    var AbstractController = require('web.AbstractController');
    var AbstractRenderer = require('web.AbstractRenderer');
    var field_utils = require('web.field_utils');
    var qweb = core.qweb;
    var Pager = require('web.Pager');
var map_controller_original = require('web_map.MapController');

map_controller_original.include({
    custom_events: _.extend({}, AbstractController.prototype.custom_events, {
        'pin_clicked': '_onPinClick',
        'get_itinerary_clicked': '_onGetItineraryClicked',
        'open_clicked': '_onOpenClicked',
        'open_explore': '_onOpenExplore',
        
    }),
    _onOpenClicked: function (ev) {
        this.trigger_up('switch_view', {
            view_type: 'form',
            res_id: ev.data.id,
            mode: 'readonly',
            model: this.modelName
        });
    },
    _onOpenExplore: function (ev) {
        this.do_action({
            name: "Lits",
            type: 'ir.actions.act_window',
            res_model: "product.template",
            target: 'current',
            view_mode: "kanban,form,tree",
            
        });
    },
    _onGetItineraryClicked: function (ev) {
        window.open('https://www.google.com/maps/dir/?api=1&destination=' + ev.data.lat + ',' + ev.data.lon);
    },

});
});