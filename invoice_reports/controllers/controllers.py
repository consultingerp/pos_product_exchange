# -*- coding: utf-8 -*-
from odoo import http

# class AccountReports(http.Controller):
#     @http.route('/account_reports/account_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_reports/account_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_reports.listing', {
#             'root': '/account_reports/account_reports',
#             'objects': http.request.env['account_reports.account_reports'].search([]),
#         })

#     @http.route('/account_reports/account_reports/objects/<model("account_reports.account_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_reports.object', {
#             'object': obj
#         })