from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class account_payment(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection([('draft', 'Draft'),
                              ('approval', 'Waiting for Approval'),
                              ('approved', 'Approved'),
                              ('posted', 'Posted'),
                              ('sent', 'Sent'),
                              ('reconciled', 'Reconciled'),
                              ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status", track_visibility='onchange')

    @api.multi
    def make_approval(self):
        self.write({'state':'approval'})
        self.message_post(body=_('Hello %s, you are Submit payment for Approval.') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])

    @api.multi
    def make_approved(self):
        self.write({'state':'approved'})
        self.message_post(body=_('Hello %s, you are Approved the payment.') % (self.env.user.name),
                          partner_ids=[self.env.user.partner_id.id])

    @api.multi
    def just_create_payment(self):
        return True

#     @api.multi
#     def btn_reject(self):
#         self.write({'state': 'draft'})

    @api.multi
    def cancel(self):
        result = super(account_payment, self).cancel()
        for each in self:
            self.message_post(body=_('Hello %s, you are Cancel the payment.') % (self.env.user.name),
                partner_ids=[self.env.user.partner_id.id])
        return result

    @api.multi
    def action_draft(self):
        res = super(account_payment, self).action_draft()
        self.message_post(body=_('Hello %s, you are set payment to Draft.') % (self.env.user.name),
                partner_ids=[self.env.user.partner_id.id])
        return res
        

    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:
            # HERE: this below condition i change
            if rec.state not in ['draft', 'approval', 'approved']:
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
            if not rec.name and rec.payment_type != 'transfer':
                raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name})
            self.message_post(body=_('Hello %s, you are Confirm the payment.') % (self.env.user.name),
                          partner_ids=[self.env.user.partner_id.id])
