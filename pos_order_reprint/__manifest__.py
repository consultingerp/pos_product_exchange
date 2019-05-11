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
#################################################################################
{
  "name"                 :  "POS Order Reprint",
  "summary"              :  "This module is use to reprint the orders in the running point of sale session.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Order-Reprint.html",
  "description"          :  """http://webkul.com/blog/odoo-pos-order-reprint/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_order_reprint&version=11.0",
  "depends"              :  ['pos_orders'],
  "data"                 :  [
                             'views/pos_config.xml',
                             'views/template.xml',
                             'reports/order_report.xml',
                             'reports/order_reprint_paperrformat.xml',
                             'reports/report_file.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_order_reprint.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  22,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}