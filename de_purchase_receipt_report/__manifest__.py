# -*- coding: utf-8 -*-
{
    'name': "Purchase Receipt Report",

    'summary': """
       Receipt Report of ODOO v11.""",

    'description': """
Qweb Purchase Receipt Report 
====================
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check <odoo>/addons/base/module/module_data.xml of the full list
    'category': 'Event',
    'version': '2.1',

    # Agregamos estas dependencias para el ejemplo, website lo ponemos para que sea editable en interfaz web
    'depends': ['base','sale','account'],
    'data': [
        # cargamos las vistas de los reportes
        # reporte sensillo recorrido en el mismo
        #'views/report_de_journal_entries_report.xml',
        # Mostramos herencia de reportes, modificamos el header y footer por defecto
        #'views/report_external_layout_header.xml',
        #'views/report_external_layout_footer.xml',
        # cargamos los reportes
        #'de_journal_entries_report_report.xml',
        'views/de_purchase_receipt_report.xml',
        'views/report_de_purchase_receipt_report.xml',
		'views/report_external_layout_header.xml'
    ],

    'demo': [
    ],

    'tests': [
    ],
}
