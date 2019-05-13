# -*- coding: utf-8 -*-
from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_claim_created = fields.Boolean(copy=False)
