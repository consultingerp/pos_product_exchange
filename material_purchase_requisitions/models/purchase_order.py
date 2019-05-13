# -*- coding: utf-8 -*-

from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    custom_requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Requisitions', 
    )
