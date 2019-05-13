#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api,fields,models
try:
	from woocommerce import API
except ImportError:
	raise ImportError('Please Install Woocommerce Python Api')
from odoo.tools.translate import _
from datetime import datetime,timedelta
from odoo.exceptions import UserError
import logging
_logger	 = logging.getLogger(__name__)

class MultiChannelSale(models.Model):
	_inherit = "multi.channel.sale"

	@api.multi
	def import_woocommerce_categories(self,parent_id=False):
		message =''
		list_category = []
		woocommerce = self.get_woocommerce_connection()
		if self.id:		
			cat_url = 'products/categories'
			category_map_data = self.env['channel.category.mappings']
			count = 0
			if parent_id and not isinstance(parent_id,(dict)):
				cat_url = cat_url+"/"+str(parent_id)
			category_data = woocommerce.get(cat_url).json()
			if 'product_categories' in category_data:
				category_data = category_data['product_categories']
			else:
				category_data = category_data['product_category']
			if isinstance(category_data,(dict)):
				category_data = [category_data]
			for category in category_data:
				if category['parent'] and not category_map_data.search([('store_category_id','=',category['parent']),('channel_id.id','=',self.id)]):
					self.import_woocommerce_categories(category['parent'])
				if not category_map_data.search([('store_category_id','=',category['id']),('channel_id.id','=',self.id)]) and not self.env['category.feed'].search([('store_id','=',category['id']),('channel_id.id','=',self.id)]):
					category_search_record = self.env['product.category'].search([('name','=',category['name']),('channel_category_ids.instance_id.id','=',self.id)])
					if category_search_record:
						mapping_dict = {
									'channel_id'		: self.id,
									'store_category_id'	: category['id'],
									'odoo_category_id'	: category_search_record.id,
									'category_name'		: category_search_record.id,
						}
						obj = self.env['channel.category.mappings']
						self._create_mapping(obj, mapping_dict)
					else:
						count = count+1
						category_dict = {
										'name'		:category['name'],
										'parent_id'	:category['parent'] or '',
										'store_id'	:category['id'],
										'channel_id':self.id,
						}
						category_rec = self.env['category.feed'].create(category_dict)
						self._cr.commit()
						list_category.append(category_rec)
			feed_res = dict(create_ids=list_category,update_ids=[])
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			self._cr.commit()
			message += str(count)+" Categories Imported!"
			return self.display_message(message)
