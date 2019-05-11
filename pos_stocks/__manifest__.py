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
  "name"                 :  "POS Stock",
  "summary"              :  "Display Stocks inside POS. Allow/Deny Order based on stocks.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.4",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Stock.html",
  "description"          :  """http://webkul.com/blog/point-of-sale-stock/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_stocks&version=11.0&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_config_view.xml',
                             'views/template.xml',
                            ],
  "demo"                 :  ['data/pos_stock_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  47,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}