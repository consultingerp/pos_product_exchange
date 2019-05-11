# -*- coding: utf-8 -*-
from odoo import http

# class Print(http.Controller):
#     @http.route('/print/print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print/print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('print.listing', {
#             'root': '/print/print',
#             'objects': http.request.env['print.print'].search([]),
#         })

#     @http.route('/print/print/objects/<model("print.print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print.object', {
#             'object': obj
#         })