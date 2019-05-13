# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'POS Default Customer',
    'version': '1.0.1',
    'category': 'Point of Sale',
    'summary': 'This module allows us to set default customer in POS Screen',
    'description': """
This module allows us to set default customer in POS Screen.
""",
    'currency': 'EUR',
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "http://www.acespritech.com",
    'price': 15.00,
    'depends': ['point_of_sale', 'base'],
    'data': [
        'views/point_of_sale.xml',
        'views/pos_register.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: