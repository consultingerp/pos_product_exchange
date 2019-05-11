# -*- coding: utf-8 -*-
from odoo import http

# class PosLogo(http.Controller):
#     @http.route('/pos_logo/pos_logo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_logo/pos_logo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_logo.listing', {
#             'root': '/pos_logo/pos_logo',
#             'objects': http.request.env['pos_logo.pos_logo'].search([]),
#         })

#     @http.route('/pos_logo/pos_logo/objects/<model("pos_logo.pos_logo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_logo.object', {
#             'object': obj
#         })