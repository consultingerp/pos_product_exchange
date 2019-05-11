from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vehicle_number = fields.Char('Vehicle No.')
    driver = fields.Char('Driver')