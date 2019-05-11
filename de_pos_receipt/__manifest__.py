# -*- coding: utf-8 -*-

{
    'name': "POS Receipt",
    'summary': "POS Receipt",
    'description': """
        This module customizes the POS receipt
    """,
    'author': "Dynexcel",
    'category': 'Point Of Sale',
    'version': '1.8',
    'depends': [
        'point_of_sale'
    ],

    'data': [
        'views/pos_config.xml',
        'views/pos.xml',
    ],
    'js': [
        # 'static/src/js/models_extend.js',
    ],
    'qweb': [
        'static/src/xml/pos_ticket_ext.xml',
    ],
    'images': [],
    'installable': True,
    'application': True
}
