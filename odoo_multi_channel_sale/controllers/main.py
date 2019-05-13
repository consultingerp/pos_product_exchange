# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.web.controllers.main import WebClient, Binary
import logging
_logger = logging.getLogger(__name__)
MAPPINGMODEL={
	'product.product':'channel.product.mappings',
	'sale.order':'channel.order.mappings',
	}
MAPPINGFIELD={
	'product.product':'erp_product_id',
	'sale.order':'odoo_order_id',
}

class Channel(http.Controller):
	@http.route(['/channel/update/mapping',],auth="public", type='json')
	def update_mapping(self, **post):
		field =MAPPINGFIELD.get(str(post.get('model')))
		model = MAPPINGMODEL.get(str(post.get('model')))
		if field and model:
			domain = [(field,'=',int(post.get('id')))]
			mappings=request.env[model].sudo().search(domain)
			for mapping in mappings:pass
				#mapping.need_sync='yes'
		return True
	#
	# @http.route([
	# '/channel/image.png',
	# '/channel/image/<xmlid>.png',
	# '/channel/image/<xmlid>/<int:width>x<int:height>.png',
	# '/channel/image/<xmlid>/<field>.png',
	# '/channel/image/<xmlid>/<field>/<int:width>x<int:height>.png',
	# '/channel/image/<model>/<id>/<field>.png',
	# '/channel/image/<model>/<id>/<field>/<int:width>x<int:height>.png'
	# ], type='http', auth="public", website=False, multilang=False)
	# def content_image(self, id=None, max_width=0, max_height=0, **kw):
	# 	if max_width:
	# 		kw['width'] = max_width
	# 	if max_height:
	# 		kw['height'] = max_height
	# 	if id:
	# 		id, _, unique = id.partition('_')
	# 		kw['id'] = int(id)
	# 		if unique:
	# 			kw['unique'] = unique
	# 	return Binary().content_image(**kw)
