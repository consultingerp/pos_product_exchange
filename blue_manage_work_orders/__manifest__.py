# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': 'Manage / Edit Work Orders',
    'category': 'Manufacturing',
    'version': '11.0.2',
    'author': 'Blue Stingray',
    'website': 'http://bluestingray.com/services/erp',
    'application': True,
    'available_in_store': True,

    # |-------------------------------------------------------------------------
    # | Short Summary
    # |-------------------------------------------------------------------------
    # |
    # | Short 1 phrase line / summary of the modules purpose. Used as a subtitle
    # | on module listings.
    # |

    'summary': 'Manage / Edit Work Orders',

    # |-------------------------------------------------------------------------
    # | Description
    # |-------------------------------------------------------------------------
    # |
    # | Long description describing the purpose / features of the module.
    # |

    'description': """
                   The Blue Stingray Manage / Edit Work Orders Module
                   ====================================================

                   Once installed, this module allows manufacturing managers in the system to modify work orders.
                   """,

    # |-------------------------------------------------------------------------
    # | Dependencies
    # |-------------------------------------------------------------------------
    # |
    # | References of all modules that this module depends on. If this module
    # | is ever installed or upgrade, it will automatically install any
    # | dependencies as well.
    # |

    'depends': ['web',
                'mrp',],

    # |-------------------------------------------------------------------------
    # | Data References
    # |-------------------------------------------------------------------------
    # |
    # | References to all XML data that this module relies on. These XML files
    # | are automatically pulled into the system and processed.
    # |

    'data': ['records/view/form/form_mrp_workorder.xml',
             'records/view/kanban/kanban_mrp_workorder.xml',
             'records/view/tree/tree_mrp_workorder.xml',],

    # |-------------------------------------------------------------------------
    # | Demo Data
    # |-------------------------------------------------------------------------
    # |
    # | A reference to demo data
    # |

    'demo': [],

    # |-------------------------------------------------------------------------
    # | Images
    # |-------------------------------------------------------------------------
    # |
    # | The banner image is what will appear in the Odoo App Store when looking
    # | at search results. It will also appear when looking at the modules. The
    # | icon is what appears in the App Area of odoo.
    # |

    'images': [
        'static/description/banner.jpg',
    ],

    # |-------------------------------------------------------------------------
    # | Is Installable
    # |-------------------------------------------------------------------------
    # |
    # | Gives the user the option to look at Local Modules and install, upgrade
    # | or uninstall. This seems to be used by most developers as a switch for
    # | modules that are either active / inactive.
    # |

    'installable': True,

    # |-------------------------------------------------------------------------
    # | Auto Install
    # |-------------------------------------------------------------------------
    # |
    # | Lets Odoo know if this module should be automatically installed when
    # | the server is started.
    # |

    'auto_install': False,

    # |-------------------------------------------------------------------------
    # | Module Pricing
    # |-------------------------------------------------------------------------
    # |
    # | This is used for http://odoo.com/apps when the module is for sale. This
    # | states how much the module costs and in what currency.
    # |

    'price': 00.00,
    'currency': 'USD'
}
