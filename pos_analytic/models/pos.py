# -*- coding: utf-8 -*-


from odoo import fields, models


class PosConfigAnalytic(models.Model):
    _inherit = 'pos.config'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        domain=[('active', '=', True)])


class PosAnalytic(models.Model):
    _inherit = 'pos.order'

    def _prepare_analytic_account(self, line):
        order = line and line.order_id or self
        if order and order.config_id:
            acc = order.config_id.account_analytic_id
            if acc and acc.id:
                return acc.id
        return False
