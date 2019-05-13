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
	def update_woocommerce_customers(self):
		update_rec = []
		count = 0
		woocommerce = self.get_woocommerce_connection()
		partner_feed_data = self.env['partner.feed']
		date = self.with_context({'name':'customer'}).get_woocommerce_update_date()
		if not date:
			return self.display_message("Please set date in multi channel configuration")
		try:
			partner_data = woocommerce.get('customers?filter[updated_at_min]='+date).json()
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in partner_data:
			raise UserError(_("Error : "+str(partner_data['errors'][0]['message'])))
		else :
			for partner in partner_data['customers']:
				check = self.env['channel.partner.mappings'].search([('store_customer_id','=',partner['id']),('type','=','contact'),('channel_id.id','=',self.id)])
				if check:
					update_record = self.env['partner.feed'].search([('store_id','=',partner['id']),('type','=','contact'),('channel_id.id','=',self.id)])
					if update_record:
						count += 1
						update_record.state = 'update'
						partner_dict = {
									'name'		: partner['first_name'],
									'last_name'	: partner['last_name'],
									'channel_id': self.id,
									'email'		: partner['email'],
									'store_id'	: partner['id']
						}
						update_record.write(partner_dict)
						update_rec.append(update_record)
					else:
						count = count +1
						partner_dict = {
									'name'		: partner['first_name'],
									'last_name'	: partner['last_name'],
									'channel_id': self.id,
									'email'		: partner['email'],
									'store_id'	: partner['id'],
						}
						partner_rec = partner_feed_data.create(partner_dict)
						partner_rec.state = 'update'
						self._cr.commit()
						update_rec.append(partner_rec)
			feed_res = dict(create_ids=[],update_ids=update_rec)
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			self.update_product_date = str(datetime.now().date())
			message = str(count)+" Customers(s) Updated! ,  "
			return self.display_message(message)
