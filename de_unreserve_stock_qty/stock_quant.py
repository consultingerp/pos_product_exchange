from odoo import api, fields, models, _


class stock_quant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def do_quant_unreserve_quantity(self):
        for each in self:
            each._update_reserved_quantity(each.product_id, each.location_id, -each.reserved_quantity, strict=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
