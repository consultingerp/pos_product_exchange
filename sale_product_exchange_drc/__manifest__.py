# -*- coding: utf-8 -*-
{
    'name': 'Sale Product Replace and Exchange Management',
    'version': '0.4',
    'summary': 'Sale Product Replace and Exchange Management',
    'description': """
        This module aims to allow Replace and Exchange of product within the warranty period,
        Flexibility for product to move either to scrap or incoming location.
    """,
    'category': 'Sales Management',
    'author': 'DRC Systems India Pvt. Ltd.',
    'website': 'http://www.drcsystems.com/',
    'depends': ['sale_stock', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_claim_view.xml',
        'data/sale_claim_sequence.xml',
        'data/damaged_location_data.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'price': 55,
    'currency': 'EUR',
}
