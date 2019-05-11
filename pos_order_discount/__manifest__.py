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
  "name"                 :  "POS Order Discount",
  "summary"              :  "This module is use to give discount in running point of sale session.",
  "category"             :  "point_of_sale",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Order-Discount.html",
  "description"          :  """http://webkul.com/blog/pos-order-discount/""",
  # "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_order_discount&version=11.0",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/pos_discount_view.xml',
                            ],
  "demo"                 :  ['data/pos_order_discount_data.xml'],
  "qweb"                 :  [
                             'static/src/xml/discount.xml',
                             'static/src/xml/pos_discount.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",

}