# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    material_requisition_count = fields.Integer(
        compute='_compute_requistions_count', 
        string='Material Requisitions Count'
    )
    material_requisition_ids = fields.One2many(
        'material.purchase.requisition',
        'workorder_id',
        string='Material Requisitions'
    )
    
    @api.multi
    @api.depends('material_requisition_ids')
    def _compute_requistions_count(self):
        for rec in self:
            rec.material_requisition_count = len(rec.material_requisition_ids)
    
    @api.multi
    def action_see_material_requisitions(self):
        self.ensure_one()
        action = self.env.ref('material_purchase_requisitions.action_material_purchase_requisition').read()[0]
        action['domain'] = [('workorder_id', '=', self.id)]
        return action