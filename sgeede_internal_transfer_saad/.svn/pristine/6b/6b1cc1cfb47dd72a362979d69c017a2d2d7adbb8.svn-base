# -*- coding: utf-8 -*-
from odoo import fields, api, models

class Move(models.Model):
    _inherit = 'stock.move'

    transfer_line_id = fields.Many2one('stock.internal.transfer.line', 'Transfer Line')