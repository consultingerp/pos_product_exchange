# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.report import report_sxw


class SalaryMonthlyStatement(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(SalaryMonthlyStatement, self).__init__(cr, uid, name, context)
        self.localcontext.update({
        }) 

class wrapped_report_salary_statement(osv.AbstractModel):
    _name = 'report.hr_payroll_monthly_statement.report_salary_statement'
    _inherit = 'report.abstract_report'
    _template = 'hr_payroll_monthly_statement.report_salary_statement'
    _wrapped_report_class = SalaryMonthlyStatement

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: