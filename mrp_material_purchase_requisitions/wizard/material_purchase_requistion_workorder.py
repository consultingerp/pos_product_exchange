# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class MaterialPurchaseRequistionWorkorderWizard(models.TransientModel):
    _name = 'material.purchase.requisition.workorder.wizard'
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
    )
    request_date = fields.Date(
        string='Requisition Date',
        default=fields.Date.today(),
        required=True,
    )
    requisition_line_ids = fields.One2many(
        'material.requisition.workorder.line.wizard',
        'requisition_id',
        string='Purchase Requisitions Line',
        required=True,
    )
    reason = fields.Text(
        'Reason for Requisition',
        required=True,
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        required=True,
    )
    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=True,
    )
    requisiton_responsible_id = fields.Many2one(
        'hr.employee',
        string='Requisition Responsible',
        required=True,
    )
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id.id
            
    @api.multi
    def create_material_requisition(self):
        active_id = self._context.get('active_id')
        requisition_obj = self.env['material.purchase.requisition']
        requisition_line_obj = self.env['material.purchase.requisition.line']
        if not self.requisition_line_ids:
            raise Warning(_('You can add material requisitions line.'))
        vals = {
                'employee_id': self.employee_id.id,
                'department_id': self.department_id.id,
                'request_date': self.request_date,
                'reason': self.reason,
                'location_id': self.location_id.id,
                'dest_location_id': self.dest_location_id.id,
                'requisiton_responsible_id' : self.requisiton_responsible_id.id,
                'workorder_id': active_id,
                }
        requisition = requisition_obj.create(vals)
        for line in self.requisition_line_ids:
                line_vals = {
                    'requisition_type': line.requisition_type,
                    'product_id' : line.product_id.id,
                    'description': line.description,
                    'qty' : line.qty,
                    'uom' : line.uom.id,
                    'requisition_id':requisition.id
                }
                requisition_line_obj.create(line_vals)
                


class MaterialPurchaseRequisitionWorkorderLineWizard(models.TransientModel):
    _name = "material.requisition.workorder.line.wizard"
    
    requisition_id = fields.Many2one(
        'material.purchase.requisition.workorder.wizard',
        string='Requisitions', 
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
    )
    description = fields.Char(
        string='Description',
        required=True,
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
        required=True,
    )
    uom = fields.Many2one(
        'product.uom',
        string='Unit of Measure',
        required=True,
    )
    requisition_type = fields.Selection(
        selection=[
            ('internal','Internal Picking'),
            ('purchase','Purchase Order'),
        ],
        string='Requisition Action',
        default='purchase',
        required=True,
    )
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            rec.description = rec.product_id.name
            rec.uom = rec.product_id.uom_id.id