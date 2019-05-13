# -*- coding: utf-8 -*-
{
    'name': "Custom Aged Partner Balance Report",

    'summary': """
        Displays the pop up as in community version.""",

    'description': """
    """,

    'author': "Dynexcel",
    'website': "",

    # Categories can be used to filter modules in modules listing
    'category': 'Account Reports',
    'version': '11.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_invoicing', 'account_reports'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_report_aged_partner_balance_view.xml',
        'wizard/report_agedpartnerbalance.xml'
    ],
}
