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
	def create_woocommerce_variants(self,data):
		variant_list = []
		attribute_list = []
		for variant in data:
			if variant['attributes']:
				attribute_list = []
				for attributes in variant['attributes']:
					attrib_name_id = self.env['channel.attribute.mappings'].search([('attribute_name.name','=',attributes['name']),('channel_id.id','=',self.id)])
					attrib_value_id = self.env['channel.attribute.value.mappings'].search([('attribute_value_name.name','=',attributes['option']),('channel_id.id','=',self.id)])
					attr = {}
					attr['name']	=	str(attributes['name'])
					attr['value']	=	str(attributes['option'])
					attr['attrib_name_id'] = attrib_name_id.store_attribute_id
					attr['attrib_value_id'] = attrib_value_id.store_attribute_value_id
					attribute_list.append(attr)
			variant_dict = {
							'image_url'  		: variant['image'][0]['src'],
							'name_value' 		: attribute_list,
							'store_id'			: variant['id'],
							'default_code'  	: variant['sku'],
							'list_price'		: variant['price'],
							'qty_available' 	: variant['stock_quantity'],
							'weight'			: variant['weight'] or "",
							# 'weight_unit'		: "kg",
							'length'			: variant['dimensions']['length'] or "",
							'width'				: variant['dimensions']['width'] or "",
							'height'			: variant['dimensions']['height'] or "",
							'dimension_unit'	: variant['dimensions']['unit'] or "",
					}
			variant_list.append((0,0,variant_dict))
		return variant_list

	@api.multi
	def import_woocommerce_attribute(self, woocommerce=False):
		attribute_list = []
		odoo_attribute_id = 0
		if not woocommerce:
			woocommerce  =  self.get_woocommerce_connection()
		multi_channel = self.env['multi.channel.sale']
		try:
			attribute_data = woocommerce.get('products/attributes').json()
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in attribute_data:
			raise UserError(_("Error : "+str(attribute_data['errors'][0]['message'])))
		else :
			for attribute in attribute_data['product_attributes']:
				attribute_map = self.env['channel.attribute.mappings'].search([('store_attribute_id','=',attribute['id']),('channel_id.id','=',self.id)])
				if not attribute_map:
					product_attributes_obj = self.env['product.attribute']
					attribute_search_record = product_attributes_obj.search(['|',('name','=',attribute['name'].lower()),'|',('name','=',attribute['name'].title()),('name','=',attribute['name'].upper())])
					if not attribute_search_record:
						odoo_attribute_id = product_attributes_obj.create({'name':attribute['name']})
					else:
						odoo_attribute_id = attribute_search_record
					attribute_list.append({
										'id'	: attribute['id'],
										'value'	: odoo_attribute_id.id,
										})
					mapping_dict = {
								'channel_id'		: self.id,
								'store_attribute_id': attribute['id'],
								'odoo_attribute_id'	: odoo_attribute_id.id,
								'attribute_name'	: odoo_attribute_id.id,
					}
					obj = self.env['channel.attribute.mappings']
					self._create_mapping(obj, mapping_dict)
					self._cr.commit()
			attr_term = self.import_woocommerce_attribute_terms(attribute_list,woocommerce)
			self._cr.commit()
			if attr_term:
				return woocommerce
			else :
				return False


	@api.multi
	def import_woocommerce_attribute_terms(self,attribute_list=False, woocommerce=False):
		if not woocommerce:
			woocommerce = self.get_woocommerce_connection()
		multi_channel = self.env['multi.channel.sale']
		odoo_attribute_value_id = 0
		for attribute in attribute_list:
			try:
				attribute_term_data = woocommerce.get('products/attributes/'+str(attribute['id'])+'/terms').json()
			except Exception as e:
				raise UserError(_("Error : "+str(e)))
			if 'errors' in attribute_term_data:
				raise UserError(_("Error : "+str(attribute_term_data['errors'][0]['message'])))
			else :
				for term in attribute_term_data['product_attribute_terms']:
					term_map = self.env['channel.attribute.value.mappings'].search([('store_attribute_value_id','=',term['id']),('channel_id.id','=',self.id)])
					if not term_map:
						product_attributes_value_obj = self.env['product.attribute.value']
						attribute_value_search_record = product_attributes_value_obj.search([
																						('attribute_id','=',attribute['value']),
																						('name','=',term['name']),
																						]
													)
						if not attribute_value_search_record:
							odoo_attribute_value_id = product_attributes_value_obj.create({'name':term['name'],'attribute_id':attribute['value']})
						else:
							odoo_attribute_value_id = attribute_value_search_record
						mapping_dict = {
									'channel_id'				: self.id,
									'store_attribute_value_id'	: term['id'],
									'odoo_attribute_value_id'	: odoo_attribute_value_id.id,
									'attribute_value_name'		: odoo_attribute_value_id.id,
									'ecom_store'				: 'woocommerce',
						}
						obj = self.env['channel.attribute.value.mappings']
						self._create_mapping(obj, mapping_dict)
						self._cr.commit()
		return True

	@api.multi
	def import_woocommerce_products(self):
		woocommerce = False
		message = ''
		woo_instance = self.import_woocommerce_attribute()
		if not woo_instance:
			raise UserError("Failed To Create Attribute Values")
		else:
			woocommerce = woo_instance
		if not woocommerce:
			woocommerce = self.get_woocommerce_connection()
		self.import_woocommerce_categories()
		list_product = []		
		count = 0
		date = self.with_context({'name':'product'}).get_woocommerce_import_date()
		if not date:
			raise UserError(_("Please set date in multi channel configuration"))
		product_tmpl = self.env['product.feed']
		try:
			product_data = woocommerce.get('products?filter[limit]=-1&filter[created_at_min]='+date).json()
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in product_data:
			raise UserError(_("Error : "+str(product_data['errors'][0]['message'])))
		else :
			for product in product_data['products']:
				variants = []
				if not self.env['channel.template.mappings'].search([('store_product_id','=',product['id']),('channel_id.id','=',self.id)]):
					categ = ""
					if product['type'] == 'variable':
						variants = self.create_woocommerce_variants(product['variations'])
					count = count + 1
					for category in product['categories']:
						category_id = self.env['category.feed'].search([('name','=',category),('channel_id.id','=',self.id)])
						if category_id:
							categ = categ+str(category_id.store_id)+","
					product_feed_dict = {'name'				: product['title'],
									'store_id'				: product['id'],
									'default_code' 			: product['sku'],
									'list_price'			: product['price'],
									'channel_id'			: self.id,
									'description'			: product['description'],
									'qty_available' 		: product['stock_quantity'],
									'feed_variants' 		: variants,
									'image_url'				: product['images'][0]['src'],
									'extra_categ_ids'		: categ,
									'ecom_store'			: 'woocommerce',
									}
					if product['downloadable'] == True or product['virtual'] == True:
						product_feed_dict['type'] = 'service'
					if not product['type'] == 'variable':
						product_feed_dict.update({
									'weight'				: product['weight'] or "",
									# 'weight_unit'			: 'kg',
									'length'				: product['dimensions']['length'] or "",
									'width'					: product['dimensions']['width'] or "",
									'height'				: product['dimensions']['height'] or "",
									'dimension_unit'		: product['dimensions']['unit'] or "",
						})
					product_rec = product_tmpl.create(product_feed_dict)
					self._cr.commit()
					list_product.append(product_rec)
			feed_res = dict(create_ids=list_product,update_ids=[])
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			self.import_product_date = str(datetime.now().date())
			message += str(count)+" Product(s) Imported!"
			return self.display_message(message)
	
	@api.multi
	def import_all_woocommerce_products(self):
		woocommerce = False
		message = ''
		woo_instance = self.import_woocommerce_attribute()
		if not woo_instance:
			raise UserError("Failed To Create Attribute Values")
		else:
			woocommerce = woo_instance
		if not woocommerce:
			woocommerce = self.get_woocommerce_connection()
		self.import_woocommerce_categories()
		list_product = []		
		count = 0
		# date = self.with_context({'name':'product'}).get_woocommerce_import_date()
		product_tmpl = self.env['product.feed']
		try:
			i=1
			while(i):
				product_data = woocommerce.get('products?page='+str(i)).json()
				if 'errors' in product_data:
					raise UserError(_("Error : "+str(product_data['errors'][0]['message'])))
				else :
					if product_data['products']:
						i = i+1
						for product in product_data['products']:
							variants = []
							if not self.env['channel.template.mappings'].search([('store_product_id','=',product['id']),('channel_id.id','=',self.id)]):
								categ = ""
								if product['type'] == 'variable':
									variants = self.create_woocommerce_variants(product['variations'])
								count = count + 1
								for category in product['categories']:
									category_id = self.env['category.feed'].search([('name','=',category),('channel_id.id','=',self.id)])
									if category_id:
										categ = categ+str(category_id.store_id)+","
								product_feed_dict = {'name'				: product['title'],
												'store_id'				: product['id'],
												'default_code' 			: product['sku'],
												'list_price'			: product['price'],
												'channel_id'			: self.id,
												'description'			: product['description'],
												'qty_available' 		: product['stock_quantity'],
												'feed_variants' 		: variants,
												'image_url'				: product['images'][0]['src'],
												'extra_categ_ids'		: categ,
												'ecom_store'			: 'woocommerce',
												}
								if not product['type'] == 'variable':
									product_feed_dict.update({
												'weight'				: product['weight'] or "",
												# 'weight_unit'			: 'kg',
												'length'				: product['dimensions']['length'] or "",
												'width'					: product['dimensions']['width'] or "",
												'height'				: product['dimensions']['height'] or "",
												'dimension_unit'		: product['dimensions']['unit'] or "",
									})
								if product['downloadable'] == True or product['virtual'] == True:
									product_feed_dict.update({'type':'service'})
								product_rec = product_tmpl.create(product_feed_dict)
								self._cr.commit()
								list_product.append(product_rec)
					else:
						i=0
			feed_res = dict(create_ids=list_product,update_ids=[])
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			# self.import_product_date = str(datetime.now().date())
			message += str(count)+" Product(s) Imported!"
			return self.display_message(message)
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
			
	@api.multi
	def import_woocommerce_products_id(self, id):
		message = ''
		woocommerce = self.get_woocommerce_connection()
		list_product = []
		product = ''
		product_tmpl = self.env['product.feed']
		try:
			product = woocommerce.get('products/'+str(id)).json()
			product = product['product']
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in product:
			raise UserError(_("Error : "+str(product['errors'][0]['message'])))
		else :
			variants = []
			if not self.env['channel.template.mappings'].search([('store_product_id','=',product['id']),('channel_id.id','=',self.id)]):
				categ = ""
				if product['type'] == 'variable':
					variants = self.create_woocommerce_variants(product['variations'])
				for category in product['categories']:
					category_id = self.env['category.feed'].search([('name','=',category),('channel_id.id','=',self.id)])
					if category_id:
						categ = categ+str(category_id.store_id)+","
				product_feed_dict = {'name'				: product['title'],
								'store_id'				: product['id'],
								'default_code' 			: product['sku'],
								'list_price'			: product['price'],
								'channel_id'			: self.id,
								'description'			: product['description'],
								'qty_available' 		: product['stock_quantity'],
								'feed_variants' 		: variants,
								'image_url'				: product['images'][0]['src'],
								'extra_categ_ids'		: categ,
								'ecom_store'			: 'woocommerce',
								}
				if product['downloadable'] == True or product['virtual'] == True:
					product_feed_dict['type'] = 'service'
				if not product['type'] == 'variable':
					product_feed_dict.update({
								'weight'				: product['weight'] or "",
								# 'weight_unit'			: 'kg',
								'length'				: product['dimensions']['length'] or "",
								'width'					: product['dimensions']['width'] or "",
								'height'				: product['dimensions']['height'] or "",
								'dimension_unit'		: product['dimensions']['unit'] or "",
					})
				product_rec = product_tmpl.create(product_feed_dict)
				self._cr.commit()
				list_product.append(product_rec)
			feed_res = dict(create_ids=list_product,update_ids=[])
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			return True