# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<https://dynexcel.com/>)
# Copyright(c): 2015-Present dynexcel.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
  "name"                 :  "MRP Subcontracting",
  "summary"              :  "Subcontracting operations in manufacturing processes",
  "category"             :  "Manufacturing",
  "version"              :  "1.2",
  "sequence"             :  1,
  "author"               :  "Dynexcel",
  "license"              :  "Other proprietary",
  "website"              :  "http://dynexcel.com",
  "description"          :  """

""",
  "live_test_url"        :  "https://youtu.be/oJ049abU_Kw",
  "depends"              :  [
                             'mrp','purchase','quality_mrp'
                            ],
  "data"                 :  [
                            'views/workcenter_view.xml',
                            'views/workorder_view.xml',
                            'views/subcontracting_order_view.xml'
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  49,
  "currency"             :  "EUR",
  "images"		 :['static/description/banner.jpg'],
}