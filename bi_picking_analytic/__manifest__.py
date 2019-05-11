# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Analytic Account on Stock Picking with Analytic Tags',
    'version': '11.0.0.5',
    'category': 'Warehouse',
    'summary': 'This apps helps to add analytic account on stock move and stock picking',
    'description': """Adds an analytic account in stock move
		Stock Picking Analytic Account, Analytic Account on Stock Picking, Analytic Account on Stock Move
		Analytic Costing on Stock Picking, Analytic costing on Stock move,Stock move analytic Account.
		Add Analytic account on picking, Add analytic costing on picking, Analytic Accounting with Stock picking,Analytic Accounting with Stock move,   Analytic Accounting with picking,Analytic Accounting with move,   
    """,
    'license':'OPL-1',
    'author': 'BrowseInfo',
    "price": 25,
    "currency": 'EUR',
    'website': '',
    'depends': ['base','sale_management','stock','analytic',"stock_account",'purchase'],
    'data': ["views/stock_move_views.xml"
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}

