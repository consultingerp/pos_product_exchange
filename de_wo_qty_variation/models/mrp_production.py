from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def close_forcefully(self):
        for workorder_rec in self.workorder_ids.filtered(lambda r: r.state != 'done'):
            if not workorder_rec.check_ids:
                workorder_rec.button_start()
                workorder_rec.do_finish()
        for workorder_rec in self.workorder_ids.filtered(lambda r: r.state != 'done'):
            print('workorder_rec  is_last_step',workorder_rec, workorder_rec.is_last_step)
            if not workorder_rec.is_last_step:
                # lot_rec = self.env['stock.production.lot'].search(
                #     [('product_id', '=', workorder_rec.component_id.id)], limit=1)
                # print('lot_rec----',lot_rec)
                # if not lot_rec:
                new_lot_rec = self.env['stock.production.lot'].create({
                    'product_id': workorder_rec.component_id.id
                })
                print('new_lot_rec---',new_lot_rec)
                workorder_rec.lot_id = new_lot_rec.id
                print('workorder_rec.lot_id---',workorder_rec.lot_id)
                workorder_rec.action_next()
            if workorder_rec.is_last_step:

                print('Last step ----',workorder_rec)
                workorder_rec.action_next()
                workorder_rec.do_finish()
        # self.button_mark_done()
