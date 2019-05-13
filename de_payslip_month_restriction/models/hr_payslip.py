# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    @api.constrains('employee_id', 'date_from', 'date_to')
    def _check_payslip_dates(self):
        if self.employee_id and self.date_from and self.date_to:
            payslip_ids = self.search([('id', '!=', self.id),
                                       ('employee_id', '=', self.employee_id.id),
                                          ('state','in',('draft', 'in_progress')),
                                        '|', '&', ('date_from','<=', self.date_from),
                                          ('date_to','>=', self.date_from),
                                          '&', ('date_from','<=', self.date_to),
                                          ('date_to','>=', self.date_from)])
            if payslip_ids:
                raise ValidationError(_("The employee already has a payslip in the given duration. "))
        return True