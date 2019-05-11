# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _

class PosOrderDiscount(models.Model):
    _name = 'pos.order.discount'

    @api.depends('discount_method', 'discount_type')
    def _discount_method_fun(self):
        res = ""
        for discount_obj in self:
            if discount_obj.discount_method:
                res = str(discount_obj.discount_method) + " ("
                res += '%)' if discount_obj.discount_type == 'percent' else 'Amount)'
            discount_obj.discount_method_function = res

    file = fields.Binary(string='File')
    name = fields.Char(string='Discount Name', help='Name of discount', required=True)
    discount_method = fields.Float(string='Discount basis', required=True)
    discount_type = fields.Selection([('percent', '%'),
                                      ('amount', 'Amount'),
                                      ], string="Discount type", required=True, default='percent')
    short_description = fields.Char(string="Short summary", help="To be displayed on POS.")
    description = fields.Text(string="Description")
    discount_on = fields.Selection([('without_tax', 'Tax Exclusive'),
                                    ('tax_inclusive', 'Tax Inclusive'),
                                    ], string="Discount Applied on", required=True, default='without_tax')
    discount_method_function = fields.Char(compute='_discount_method_fun', string='Discount basis')

class PosConfig(models.Model):
    _inherit = 'pos.config'

    wk_discount_product_id = fields.Many2one('product.product', string='Discount Product', domain=[
                                             ('type', '=', 'service')], help='The product used to model the discount')
    wk_discounts = fields.Many2many('pos.order.discount', 'confing_discount_rel', 'wk_confing_id', 'wk_discount_id', string='Discounts')


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        if ui_order.get('discountLine'):
            res['lines'].append(ui_order['discountLine'][0])
        return res
