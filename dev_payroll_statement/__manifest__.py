# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

{
    'name': 'Employee Payroll Statement',
    'version': '11.0.1.2',
    'category': 'HR',
    'sequence':1,
    'summary': 'App will print employee payroll monthly statement with salary rules',
    'description': """
        App will print employee payroll monthly statement with salary rules

Employee payslip statement, payroll statement, hr payslip statement, hr payroll , hr employee payroll, payroll summary report, emploee payslip by monthly, payslip ragistar, employee payslip generator, payslip salary rule , employee salary rule

            """,
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'depends': ['hr_payroll'],
    'data': [
        'wizard/emp_payroll_statement_view.xml',
        'views/payroll_statement_tempate.xml',
        'views/payroll_statement_report_menu.xml',        
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':39.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/TpBgCFsyOsc',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
