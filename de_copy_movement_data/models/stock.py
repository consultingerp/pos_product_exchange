from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_transfer(self):
        res = super(StockPicking, self).do_transfer()
        for picking in self:
            for each_group_picking in self.search([('group_id','=',picking.group_id.id),
                                                  ('id', '!=', picking.id)]):
                each_group_picking.vehicle_number = picking.vehicle_number
                each_group_picking.driver = picking.driver
                for pack in each_group_picking.pack_operation_ids:
                    if pack.product_qty > 0:
                        pack.write({'qty_done': pack.product_qty})
                    else:
                        pack.unlink()

        return res