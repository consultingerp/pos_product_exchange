
{
    'name': "invoice_reports",

    'summary': """
        Inherit the qweb reports of Account.invoice""",

    'description': """
        Inherit the qweb reports of Account.invoice
    """,

    'author': "Hassan Ali(Dynexcel)",
    'website': "http://www.dynexcel.com",

  
    'category': 'Qweb',
    'version': '0.1',

    
    'depends': ['account'],

    
    'data': [
        # 'security/ir.model.access.csv',
       # 'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}