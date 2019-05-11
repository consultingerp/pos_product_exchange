from odoo import models,fields,api


class AccountAsset(models.Model):
    _inherit = 'account.asset.asset'

    barcode = fields.Char('Barcode')
    location_id = fields.Many2one('stock.location', 'Location')
    physical_location = fields.Char('Physical Location')
