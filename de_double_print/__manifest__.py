# -*- coding: utf-8 -*-
{
    'name': "Double print",

    'summary': """
        this module will send double print command""",

    'description': """
        it extend the point sale screen widget .
		It will override the existing print function with new one that will send print command two times
    """,

    'author': "DX",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Web',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}