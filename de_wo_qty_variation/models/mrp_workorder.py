from odoo import api, fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.multi
    def record_production(self):
        res = super(MrpWorkorder, self).record_production()
        if self.next_work_order_id:
            print('My code----Trueeee', self.next_work_order_id)
            self.next_work_order_id.qty_producing = self.qty_produced
        return res
