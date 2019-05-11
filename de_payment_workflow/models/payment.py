# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<https://dynexcel.com/>)
# Copyright(c): 2015-Present dynexcel.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PaymentState(models.Model):
    _name = 'account.payment_state'
    _description = 'Partners Payment'

    name = fields.Char(string='Payment Status',help='maintain the states of the payment document')
    authority = fields.Many2one('res.groups')

class account_payment(models.Model):
    _inherit = 'account.payment'
    _description = 'this class maintain the approvals of the payments. '

    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('approved', 'approved'),
                              ('posted', 'Posted'),
                              ('sent', 'Sent'),
                              ('reconciled', 'Reconciled'),
                              ('cancelled', 'Cancelled')],
                             readonly=True, default='draft', copy=False, string="Status", track_visibility='onchange')

    @api.multi
    def action_draft(self):
        res = super(account_payment, self).action_draft()
        self.message_post(body=_('Dear %s, you are set payment to Draft.') % (self.env.user.name),
                          partner_ids=[self.env.user.partner_id.id])
        return res

    @api.multi
    def submit_payment(self):
        self.write({'state': 'submit'})
        self.message_post(body=_('Dear %s, payment is submitted for Approval.') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])

    @api.multi
    def approve_payment(self):
        self.write({'state': 'approved'})
        self.message_post(body=_('Dear %s, payment has approved.') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])

    @api.multi
    def cancel(self):
        for rec in self:
            for move in rec.move_line_ids.mapped('move_id'):
                if rec.invoice_ids:
                    move.line_ids.remove_move_reconcile()
                move.button_cancel()
                move.unlink()
            rec.state = 'cancelled'
    #
    # @api.multi
    # def unlink(self):
    #     if any(bool(rec.move_line_ids) for rec in self):
    #         raise UserError(_("You cannot delete a payment that is already posted."))
    #     if any(rec.move_name for rec in self):
    #         raise UserError(_(
    #             'It is not allowed to delete a payment that already created a journal entry since it would create a gap in the numbering. You should create the journal entry again and cancel it thanks to a regular revert.'))
    #     return super(account_payment, self).unlink()

    @api.multi
    def just_create_payment(self):
        return True

    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
                    A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
                    and another in the destination reconcilable account (see _compute_destination_account_id).
                    If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
                    If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
                """
        for rec in self:

            if rec.state not in ['draft', 'approved']:
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if rec.name in ('', 'Draft Payment'):
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

                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
                sequence_code)
            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(
                    lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

        rec.write({'state': 'posted', 'move_name': move.name})

        self.message_post(body=_('Dear %s, payment has confirmed.') % (self.env.user.name,),
                              partner_ids=[self.env.user.partner_id.id])
        return res


