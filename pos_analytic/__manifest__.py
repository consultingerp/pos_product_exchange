# -*- coding: utf-8 -*-
{
    'name': "POS Analytic",
    'description': """Analytic accounting for Point of Sale""",
    'category': 'Point Of Sale',
    'author': 'ERP Ukraine',
    'website': 'https://erp.co.ua',
    'support': 'support@erp.co.ua',
    'license': 'AGPL-3',
    'version': '1.0',
    'price': 30.00,
    'currency': 'EUR',
    'depends': ['analytic', 'point_of_sale'],
    'data': ['views/pos.xml'],
    'installable': True,
    'application': True,
}
