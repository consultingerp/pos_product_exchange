# -*- coding: utf-8 -*-

from odoo import models,fields

class SubcontractOrder(models.Model):
    _inherit = 'stock.picking'
    
    subcontract_id = fields.Many2one('subcontract.order','Sub-Contract Order')