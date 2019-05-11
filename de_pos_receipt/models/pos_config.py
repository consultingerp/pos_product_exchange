from odoo import api, fields,models

class PosConfig(models.Model):
	_inherit = 'pos.config'

	is_partner_pos = fields.Boolean(string='Customer POS', default=False)
