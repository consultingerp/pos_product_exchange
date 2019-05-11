# -*- coding: utf-8 -*-
{
    'name': "pos_logo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hassan Ali",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'web',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','point_of_sale','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
	
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb':[
	'static/src/xml/poschange.xml',
	'static/src/xml/sources.xml'
	],
    'installable': True,
    'application': True,
    'auto_install': False,
}
