from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    claim_id = fields.Many2one('sale.claim')

    @api.multi
    def open_claim_invoice(self):
        action = {}
        action_id = self.env.ref('account.action_invoice_tree2')
        if action_id:
            action = action_id.read()
            action = action[0] or action
            action['domain'] = "[('id','in', [" + ','.join(map(str, self.ids)) + "])]"
            return action
        return True
