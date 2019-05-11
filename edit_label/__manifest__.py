# -*- coding: utf-8 -*-
{
    'name': "edit_label",

    'summary': """
        this module will change label(tax id or tin) at res.partner form view""",

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
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml'
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}