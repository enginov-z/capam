# -*- coding: utf-8 -*-
from odoo import http
import json

class MyModule(http.Controller):
    @http.route('/rea_management/hospitals_ocupied/', type='http', auth='public')
    def index(self, **kw):
        l = []
        for x in http.request.env['res.company'].search([]):
            o = x.x_studio_lit_totals -  x.x_studio_lits_disponible 
            l.append({
                'occ':o,
                'name':x.name
            })
        return http.request.make_response(json.dumps(l), [('Content-Type', 'application/json')])
    @http.route('/rea_management/hospitals_free/', type='http', auth='public')
    def index1(self, **kw):
        l = []
        for x in http.request.env['res.company'].search([]):
            l.append({
                'free':x.x_studio_lits_disponible,
                'name':x.name
            })
        return http.request.make_response(json.dumps(l), [('Content-Type', 'application/json')])
    @http.route('/rea_management/hospitals_total/', type='http', auth='public')
    def index2(self, **kw):
        l = []
        for x in http.request.env['res.company'].search([]):
            l.append({
                'tot':x.x_studio_lit_totals,
                'name':x.name
            })
        return http.request.make_response(json.dumps(l), [('Content-Type', 'application/json')])
 
    @http.route('/rea_management/hospitals_general_availability/', type='http', auth='public')
    def index3(self, **kw):
        l=[]
        free = 0
        occupied = 0 
        for x in http.request.env['res.company'].search([]):
            occupied += (x.x_studio_lit_totals -  x.x_studio_lits_disponible)
            free += x.x_studio_lits_disponible
            l.append({
                'free':free,
                'occupied':free
            })
        return http.request.make_response(json.dumps(l), [('Content-Type', 'application/json')])


#     @http.route('/my_module/my_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_module.listing', {
#             'root': '/my_module/my_module',
#             'objects': http.request.env['my_module.my_module'].search([]),
#         })

#     @http.route('/my_module/my_module/objects/<model("my_module.my_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_module.object', {
#             'object': obj
#         })