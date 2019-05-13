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

    # @api.multi
    # def cancel(self):
    #     for rec in self:
    #         for move in rec.move_line_ids.mapped('move_id'):
    #             if rec.invoice_ids:
    #                 move.line_ids.remove_move_reconcile()
    #             move.button_cancel()
    #             move.unlink()
    #         rec.state = 'cancelled'
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
        self.write({'state': 'draft'})
        res = super(account_payment, self).post()
        self.message_post(body=_('Dear %s, payment has posted') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])
        return res