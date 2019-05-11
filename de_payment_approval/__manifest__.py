# -*- coding: utf-8 -*-
{
    'name': 'Payment Approval',
    'version': '11.0.2',
    'category': 'Accounting',
    'description': """
""",
    'depends': [
        'base',
        'account_invoicing',
        'account_cancel'
    ],
    'data': [
#         'security/ir.model.access.csv',
        'account_user.xml', 
        'account_view.xml',
    ],
    'application': False,
    'license': 'OPL-1',
}
