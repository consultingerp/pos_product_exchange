# -*- coding: utf-8 -*-
from odoo import api, models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def align_workorders(self):
        """
        Align all the work orders on this work order by sorting by sequence and
        resetting both sequencing and next work orders. This exists because when
        new work orders are created, they need to be properly setup in the
        sequence chain.

        :return: None
        """
        for production_id in self:
            num_workorders = len(production_id.workorder_ids)
            workorder_ids = production_id.workorder_ids.sorted(key=lambda record: record.sequence)

            for count, workorder_id in enumerate(workorder_ids):
                next_workorder_id = False
                if count < num_workorders - 1:
                    next_workorder_id = production_id.workorder_ids[count + 1].id

                workorder_id.update({'next_work_order_id': next_workorder_id,
                                     'sequence': count})
