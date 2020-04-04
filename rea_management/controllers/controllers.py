# -*- coding: utf-8 -*-
from odoo import http

# class ReaManagement(http.Controller):
#     @http.route('/rea_management/rea_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rea_management/rea_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rea_management.listing', {
#             'root': '/rea_management/rea_management',
#             'objects': http.request.env['rea_management.rea_management'].search([]),
#         })

#     @http.route('/rea_management/rea_management/objects/<model("rea_management.rea_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rea_management.object', {
#             'object': obj
#         })