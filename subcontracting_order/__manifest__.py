# -*- coding: utf-8 -*-

{'name': 'Subcontracting Order',
 'version': '11.0.1.0.0',
 'category': 'other',
 'depends': ['account',
             'sale_stock','purchase'
             ],
 'author': "Dynexl",
 'license': 'AGPL-3',
 'website': '',
 'data': [
        'security/ir.model.access.csv',
        'views/sub_contract_view.xml',
        'data/ir_sequence_data.xml',
        ],
 'installable': True,
 'application': True,
 }