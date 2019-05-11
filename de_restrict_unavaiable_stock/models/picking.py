from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"
    
    @api.multi
    def button_validate(self):

        for rec in self:
            source_location = rec.location_id
            if rec.picking_type_id and rec.picking_type_id.code == 'outgoing':
                for move_rec in rec.move_lines:
                    if self.env['stock.quant']._get_available_quantity(move_rec.product_id,source_location,lot_id=None, package_id=None, owner_id=None, strict=False) < move_rec.quantity_done:
                        raise UserError(_('%s quantity is not enough!' %(move_rec.product_id.name)))
        return super(Picking, self).button_validate()
