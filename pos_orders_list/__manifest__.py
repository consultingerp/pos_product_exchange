# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS Order List",
    "version" : "11.0.0.2",
    "category" : "Point of Sale",
    "depends" : ['base','sale','point_of_sale'],
    "author": "BrowseInfo",
    'summary': ' ',
    'price': '15.00',
    'currency': "EUR",
    "description": """
    
    Purpose :- 
see the list of all the orders within a running POS Screen. It shows the Pos All Orders List on POS screen. View all POS order on screen. List all POS order on POS screen. Show order on POS, view all orders on POS, Display order on POS, View order on POS
    """,
    "website" : "www.browseinfo.in",
    "data": [
        'views/custom_pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_orders_list.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
