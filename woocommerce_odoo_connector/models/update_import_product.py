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
from odoo.addons.odoo_multi_channel_sale.tools import extract_list as EL
from odoo.exceptions import UserError
import logging
_logger	 = logging.getLogger(__name__)

class MultiChannelSale(models.Model):
	_inherit = "multi.channel.sale"

	@api.multi
	def update_woocommerce_products(self, woocommerce=False):
		update_rec = []
		categ = ''
		count = 0
		# self.import_woocommerce_attribute()
		# self.import_woocommerce_categories()
		if not woocommerce:
			woocommerce = self.get_woocommerce_connection()
		date = self.with_context({'name':'product'}).get_woocommerce_update_date()
		if not date:
			raise UserError(_("Please set date in multi channel configuration"))
		product_tmpl = self.env['product.feed']
		try:
			product_data = woocommerce.get('products?filter[limit]=-1&filter[updated_at_min]='+date).json()
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in product_data:
			raise UserError(_("Error : "+str(product_data['errors'][0]['message'])))
		else :
			for product in product_data['products']:
				variants = []
				check = self.env['channel.template.mappings'].search([('store_product_id','=',product['id']),('channel_id.id','=',self.id)])
				if check:
					update_record = product_tmpl.search([('store_id','=',product['id']),('channel_id.id','=',self.id)])
					if update_record:
						count += 1
						update_record.state = 'update'
						# if product['downloadable'] == True or product['virtual'] == True:
						# 	continue
						if product['type'] == 'variable':
							update_record.write({'feed_variants':[(5,),]})
							variants = self.create_woocommerce_variants(product['variations'])
						for category in product['categories']:
							category_id = self.env['category.feed'].search([('name','=',category),('channel_id.id','=',self.id)])
							if category_id:
								categ = categ+str(category_id.store_id)+","
						product_feed_dict = {'name'					: product['title'],
											'store_id'				: product['id'],
											'default_code'  		: product['sku'],
											'list_price'			: product['price'],
											'channel_id'			: self.id,
											'description'			: product['description'],
											#'qty_available'		: product['stock_quantity'],
											'feed_variants' 		: variants,
											'image_url'				: product['images'][0]['src'],
											'extra_categ_ids'		: categ,
											'weight'				: product['weight'] or "",
											# 'weight_unit'			: 'kg',
											'length'				: product['dimensions']['length'] or "",
											'width'					: product['dimensions']['width'] or "",
											'height'				: product['dimensions']['height'] or "",
											'dimension_unit'		: product['dimensions']['unit'] or "",
						}
						update_record.write(product_feed_dict)
						self._cr.commit()
						update_rec.append(update_record)
					else:
						if product['downloadable'] == True or product['virtual'] == True:
							product_feed_dict['type'] = 'service'
						if product['type'] == 'variable':
							variants = self.create_woocommerce_variants(product['variations'])
						count = count + 1
						for category in product['categories']:
							category_id = self.env['category.feed'].search([('name','=',category),('channel_id.id','=',self.id)])
							if category_id:
								categ = categ+str(category_id.store_id)+","
						product_feed_dict = {'name'				: product['title'],
										'store_id'				: product['id'],
										'default_code'  		: product['sku'],
										'list_price'			: product['price'],
										'channel_id'			: self.id,
										'description'			: product['description'],
										#'qty_available'		: product['stock_quantity'],
										'feed_variants' 		: variants,
										'image_url'				: product['images'][0]['src'],
										'extra_categ_ids'		: categ,
										'ecom_store'			: 'woocommerce',
										'weight'				: product['weight'] or "",
										# 'weight_unit'			: 'kg',
										'length'				: product['dimensions']['length'] or "",
										'width'					: product['dimensions']['width'] or "",
										'height'				: product['dimensions']['height'] or "",
										'dimension_unit'		: product['dimensions']['unit'] or "",
										}
						product_rec = product_tmpl.create(product_feed_dict)
						product_rec.state = 'update'
						self._cr.commit()
						update_rec.append(product_rec)
			feed_res = dict(create_ids=[],update_ids=update_rec)
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			self.update_product_date = str(datetime.now())
			message = str(count)+" Product(s) Updated! , "
			return self.display_message(message)
