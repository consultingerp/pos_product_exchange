# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
###################################################################################
{
  "name"                 :  "Woocommerce Odoo Connector",
  "summary"              :  "Woocommerce Odoo Connector extension  provides in-depth integration with Odoo and Woocommerce.",
  "category"             :  "Bridge",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "http://www.webkul.com",
  "description"          :  """====================
**Help and Support**
====================
.. |icon_features| image:: woocommerce_odoo_connector/static/src/img/icon-features.png
.. |icon_support| image:: woocommerce_odoo_connector/static/src/img/icon-support.png
.. |icon_help| image:: woocommerce_odoo_connector/static/src/img/icon-help.png

|icon_help| `Help <https://webkul.com/ticket/open.php>`_ |icon_support| `Support <https://webkul.com/ticket/open.php>`_ |icon_features| `Request new Feature(s) <https://webkul.com/ticket/open.php>`_""",
  "live_test_url"        :  "http://wpodoo.webkul.com/woocommerce_odoo_connector/",
  "depends"              :  ['odoo_multi_channel_sale'],
  "data"                 :  [
                             'views/woc_config_views.xml',
                             'data/import_cron.xml',
                             'data/default_data.xml',
                             'views/inherited_woocommerce_dashboard_view.xml',
                             'wizard/import_update_wizard.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  100,
  "currency"             :  "EUR",
  "external_dependencies":  {'python': ['woocommerce']},
}