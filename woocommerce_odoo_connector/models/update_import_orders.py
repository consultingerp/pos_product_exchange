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
	def update_woocommerce_orders(self, woocommerce=False):
		update_rec = []
		count = 0
		if not woocommerce:
			woocommerce = self.get_woocommerce_connection()
		order_feed_data = self.env['order.feed']
		date = self.with_context({'name':'order'}).get_woocommerce_update_date()
		if not date:
			raise UserError(_("Please set date in multi channel configuration"))
		try:
			order_data = woocommerce.get('orders?filter[limit]=-1&filter[updated_at_min]='+date).json()
		except Exception as e:
			raise UserError(_("Error : "+str(e)))
		if 'errors' in order_data:
			raise UserError(_("Error : "+str(order_data['errors'][0]['message'])))
		else :
			for order in order_data['orders']:
				update_record = self.env['order.feed'].search([('store_id','=',order['id']),('channel_id.id','=',self.id)])
				if update_record and update_record.order_state != order['status']:
					count += 1
					update_record.state = 'update'
					order_dict = {
								'order_state': order['status']
					}
					update_record.write(order_dict)
					update_rec.append(update_record)
			feed_res = dict(create_ids=[],update_ids=update_rec)
			self.env['channel.operation'].post_feed_import_process(self,feed_res)
			self.update_order_date = str(datetime.now().date())
			message = str(count)+" Order(s) Updated! , "
			return self.display_message(message)
