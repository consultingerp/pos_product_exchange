from odoo import models,fields,api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    partner_id = fields.Many2one('res.partner', 'Partner')
    service_product_id = fields.Many2one('product.product', 'Product', domain=[('type','=','service')])
    delivery_type_id = fields.Many2one('stock.picking.type', 'Picking Type')
    return_type_id = fields.Many2one('stock.picking.type', 'Return Type')
    cost_per_qty = fields.Float('Cost per Qty')
    is_subcontracting = fields.Boolean('Is Subcontracting')
