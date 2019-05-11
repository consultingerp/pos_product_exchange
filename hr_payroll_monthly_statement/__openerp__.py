# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': "HR Employees Payroll Monthly Statement",
    'version': '1.3',
    'price': 49.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources',
    'summary':  """This module allow HR to print pdf report for payroll statement.""",
    'description': """
        HR Payroll Monthly Statement Modules:
        - Payroll Monthly Statement

payroll monthly statement
hr_payroll
payroll statement   
hr payroll
payroll
payslips report
payslip report
summary payroll
summary payslip
monthly statement
payroll register
print payslip
payslip register
payslip in excel
payroll statement
payslip statement
employee payroll statement
monthly report payroll
payroll monthly report
payroll monthly statement
hr report
hr monthly statement
payslip statement
employee statement monthly
payroll report statement
monthly report payroll
payroll excel
excel report
    """,
    
    'author': "Probuse Consulting Service Pvt Ltd",
    'website': "www.probuse.com",
    'images': ['static/description/123.jpg'],
    'depends': ['hr_payroll', 'hr_attendance'],
    'live_test_url': 'https://youtu.be/vMejiHQnoys',
    'data': [
         "security/ir.model.access.csv",
        'wizard/salary_monthly_statement.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
