# -*- coding: utf-8 -*-
from odoo import http

# class EditLabel(http.Controller):
#     @http.route('/edit_label/edit_label/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_label/edit_label/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_label.listing', {
#             'root': '/edit_label/edit_label',
#             'objects': http.request.env['edit_label.edit_label'].search([]),
#         })

#     @http.route('/edit_label/edit_label/objects/<model("edit_label.edit_label"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_label.object', {
#             'object': obj
#         })