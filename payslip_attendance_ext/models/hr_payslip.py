# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
#     @api.model
#     def create(self,vals):
#         res = super(HrPayslip,self).create(vals)
#         #For faster performance used query.
#         if res.date_from and res.date_to and res.contract_id:
#             self._cr.execute("select count(id) from hr_attendance where check_in::date>='%s' and check_out::date<='%s' and employee_id=%d"%(res.date_from,res.date_to,res.employee_id.id))
#             result = self._cr.fetchone()
#             if result and result[0]:
#                 self.env['hr.payslip.worked_days'].create({'name': '%s Attendances'%(res.employee_id.name),'number_of_days':result[0], 'code' : 'Attendance', 'payslip_id':res.id,'contract_id':res.contract_id.id})
#         return res
# 
    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        lst = []
        if self.date_from and self.date_to and self.contract_id:
            self._cr.execute("select count(id) from hr_attendance where check_in::date>='%s' and check_out::date<='%s' and employee_id=%d" % (self.date_from, self.date_to, self.employee_id.id))
            result = self._cr.fetchone()
            if result and result[0]:
                lst.append({'name': '%s Attendances' % (self.employee_id.name),
                            'number_of_days': result[0],
                            'code' : 'Attendance',
                            'contract_id': self.contract_id.id})
            # leave
            self._cr.execute("""select sum(number_of_days_temp)
                                from hr_holidays
                                where date_from::date >= '%s'
                                and date_to::date <= '%s'
                                and state = 'validate'
                                and type = 'remove'
                                and employee_id='%s'""" % (self.date_from, self.date_to, self.employee_id.id))
            result = self._cr.fetchone()
            print ("\n\n --payslip_attendance_ext--", result)
            if result:
                lst.append({'name': '%s Leave' % (self.employee_id.name),
                            'number_of_days': result[0] if result[0] else 0.00,
                            'code' : 'Leave',
                            'contract_id': self.contract_id.id})
        #self.worked_days_line_ids = False
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in lst:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids += worked_days_lines
        return res
