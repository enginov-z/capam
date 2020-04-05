odoo.define('map_render_custom',function(require){
var map_renderer_original = require('web_map.MapRenderer');

map_renderer_original._addMakers.include(function(){
    console.log('haha i worked')
})

});