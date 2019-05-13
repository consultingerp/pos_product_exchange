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
  "name"                 :  "POS All Orders List",
  "summary"              :  "POS All Orders List module display all old orders and this model is linked with POS order return, POS order reprint and POS Reorder.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.1.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-All-Orders-List.html",
  "description"          :  """https://webkul.com/blog/odoo-pos-all-orders-list/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_orders&version=11.0",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_config_view.xml',
                             'views/template.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_orders.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  27,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}