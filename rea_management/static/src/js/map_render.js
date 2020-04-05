odoo.define('map_render_custom',function(require){
    var core = require('web.core');
    var AbstractRenderer = require('web.AbstractRenderer');
    var field_utils = require('web.field_utils');
    var qweb = core.qweb;
var map_renderer_original = require('web_map.MapRenderer');

map_renderer_original.include({
    _addMakers: function (records) {
        console.log('lol in your face odoo , i did it')
        var self = this;
        this._removeMakers();
        records.forEach(function (record) {
            if (record.partner && record.partner.partner_latitude && record.partner.partner_longitude) {
                var popup = {};
                popup.records = self._getMarkerPopupFields(record, self.fieldsMarkerPopup);
                popup.url = 'https://www.google.com/maps/dir/?api=1&destination=' + record.partner.partner_latitude + ',' + record.partner.partner_longitude;
                var $popup = $(qweb.render('map-popup', { records: popup }));
                var openButton = $popup.find('button.btn.btn-primary.edit')[0];
                if (self.hasFormView) {
                    openButton.onclick = function () {
                        self.trigger_up('open_clicked',
                            { id: record.id });
                    };
                } else {
                    openButton.remove();
                }

                var marker;
                var offset;

                if (self.numbering) {
                    var number = L.icon({
                        className: 'o_numbered_marker',
                        html: '<p class ="o_number_icon">' + (self.state.records.indexOf(record) + 1) + '</p>',
                        iconUrl: '/rea_management/static/src/img/marker-blue.png',
                    });
                    marker = L.marker([record.partner.partner_latitude, record.partner.partner_longitude], { icon: number });
                    offset = new L.Point(0, -35);

                } else {
                    var number = L.icon({
                        className: 'o_numbered_marker',
                        html: '<p class ="o_number_icon">' + (record.x_studio_lits_disponible ) + '</p>',
                        iconUrl: '/rea_management/static/src/img/marker-blue.png',
                    });
                    marker = L.marker([record.partner.partner_latitude, record.partner.partner_longitude], { icon: number });
                    offset = new L.Point(0, -35);
                }
                marker
                    .addTo(self.leafletMap)
                    .bindPopup(function () {
                        var divPopup = document.createElement('div');
                        $popup.each(function (i, element) {
                            divPopup.appendChild(element);
                        });
                        return divPopup;
                    }, { offset: offset });
                self.markers.push(marker);
            }
        });
    },
})

});