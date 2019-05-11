from odoo import models, fields, api


class pos_order(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_new_job(self, config_id, order_id):
        config_id = self.env['pos.config'].browse(config_id)
        x = config_id.sequence_id._next()
        print ("\n\n --x---", x, order_id)
        return config_id.name

    display_name_copy = fields.Char(related='name', store=True)

class pos_config(models.Model):
    _inherit = 'pos.config'

    is_customer_pos = fields.Boolean(string='Customer POS')