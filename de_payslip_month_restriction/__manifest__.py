# -*- coding: utf-8 -*-
{
    'name' : 'Payslip Restriction for a Month',
    'version': '1.0',
    'author' : 'DX',
    'website' : '',
    'category' : '',
    'summary': 'This module will restrict user to generate multiple payslips for an employee.',
    'description': """

This module will restrict user to generate multiple payslips for an employee

            """,
    'depends':['hr', 'hr_payroll'],
    'data' : ['views/payslip_view.xml'],
    'installable':True,
    'auto_install':False
}

