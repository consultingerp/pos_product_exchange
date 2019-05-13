# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS Order Return",
    "version" : "11.0.0.0",
    "category" : "Point of Sale",
    'summary': 'This apps allow to return order and product from the Point of Sale Screen.',
    "depends" : ['base','sale','point_of_sale','pos_orders_list'],
    "author": "BrowseInfo",
    'summary': 'This apps helps to return product from POS screen as well as retrun whole order from POS screen',
    'price': '20',
    'currency': "EUR",
    "description": """
This Module Helps a return orders from the POS.Also it helps to return the product from POS. Also able to return whole order from POS screen.
Return product from POS screen. Return product from POS Screen.POS return product, POS product return. POS order return. Order Return from POS, Product Return from POS,POS Revise Order, POS Product Return, Revise POS Order, Cancel POS Order,Cancel Order.
    """,
    "website" : "www.browseinfo.in",
    "data": [
        'views/custom_pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_return_order.xml',
    ], 
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
