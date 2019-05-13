# -*- coding: utf-8 -*-
from odoo import api, models, fields


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'
    _order = 'production_id,sequence'

    sequence = fields.Integer(string='Sequence', default=100)

    @api.model
    def create(self, vals):
        """
        Inherit `create` to force work order alignment. See `mrp.production`
        method `align_workorders` for more information.

        :param vals: A Dictionary of fields and their values
        :return: The new `mrp.workorder` browse record
        """
        res = super(MrpWorkOrder, self).create(vals)

        if res.production_id:
            res.production_id.align_workorders()

        return res
