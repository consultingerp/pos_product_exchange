from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    store_order_id = fields.Char(related='channel_mapping_ids.store_order_id', string='Store Order ID')
