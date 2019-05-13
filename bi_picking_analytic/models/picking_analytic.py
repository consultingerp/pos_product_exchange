# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.tools.float_utils import float_is_zero, float_compare
from datetime import datetime





class ProcurementRule(models.Model):
	_inherit = 'procurement.rule'
	
	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
		result = super(ProcurementRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
		
		result.update({
			'analytic_account_id':values.get('analytic_account_id',0),
			'tag_ids':values.get('tag_ids',0),

			})
		return result




	
class SaleOrderLine(models.Model):
	
	_inherit = 'sale.order.line'
	
	
 
	@api.multi
	def _prepare_procurement_values(self,group_id):
		res = super(SaleOrderLine,self)._prepare_procurement_values(group_id=group_id)
		tag_ids = []
		for tag in self.analytic_tag_ids:
			tag_ids.append(tag.id)
		res.update({
			'analytic_account_id':self.order_id.analytic_account_id.id,
			'tag_ids':[(6,0,tag_ids)],
			})
		return res

class PurchaseOrderLine(models.Model):
	
	_inherit = 'purchase.order.line'
	
	@api.multi
	def _prepare_stock_moves(self, picking):
		""" Prepare the stock moves data for one order line. This function returns a list of
		dictionary ready to be used in stock.move's create()
		"""
		self.ensure_one()
		res = []
		tag_ids = []
		for tag in self.analytic_tag_ids:
			tag_ids.append(tag.id)
		if self.product_id.type not in ['product', 'consu']:
			return res
		qty = 0.0
		price_unit = self._get_stock_move_price_unit()
		for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
			qty += move.product_uom._compute_quantity(move.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
		template = {
			'name': self.name or '',
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'date': self.order_id.date_order,
			'date_expected': self.date_planned,
			'location_id': self.order_id.partner_id.property_stock_supplier.id,
			'location_dest_id': self.order_id._get_destination_location(),
			'picking_id': picking.id,
			'partner_id': self.order_id.dest_address_id.id,
			'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
			'state': 'draft',
			'analytic_account_id':self.account_analytic_id.id,
			'tag_ids':[(6,0,tag_ids)],
			'purchase_line_id': self.id,
			'company_id': self.order_id.company_id.id,
			'price_unit': price_unit,
			'picking_type_id': self.order_id.picking_type_id.id,
			'group_id': self.order_id.group_id.id,
			'origin': self.order_id.name,
			'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
			'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
		}
		diff_quantity = self.product_qty - qty
		if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
			quant_uom = self.product_id.uom_id
			get_param = self.env['ir.config_parameter'].sudo().get_param
			if self.product_uom.id != quant_uom.id and get_param('stock.propagate_uom') != '1':
				product_qty = self.product_uom._compute_quantity(diff_quantity, quant_uom, rounding_method='HALF-UP')
				template['product_uom'] = quant_uom.id
				template['product_uom_qty'] = product_qty
			else:
				template['product_uom_qty'] = diff_quantity
			res.append(template)
		return res


class StockMove(models.Model):
	_inherit = "stock.move"

	analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')
	tag_ids  = fields.Many2many('account.analytic.tag', string= 'Tag')

class StockPicking(models.Model):
	_inherit = "stock.picking"

	@api.multi
	def button_validate(self):
		sale_list=[]
		ref = self.name
		sale_analytic_dict={}
		purchase_analytic_dict={}
		if self.sale_id :
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids = []
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)  
					sale_analytic_dict.update({
						'name': line.sale_line_id.product_id.name,
						'amount': line.sale_line_id.price_unit,
						'product_id': line.sale_line_id.product_id.id,
						'product_uom_id': line.sale_line_id.product_uom.id,
						'date': line.date_expected,
						'account_id': line.analytic_account_id.id,
						'unit_amount': line.quantity_done,
						'general_account_id': self.partner_id.property_account_receivable_id.id,
						'ref': ref,
						'tag_ids':[(6,0,tag_ids)]
					})
					self.env['account.analytic.line'].create(sale_analytic_dict)


		if self.purchase_id :
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids = []    
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)
					purchase_analytic_dict.update({
						'name': line.purchase_line_id.product_id.name,
						'date': line.date_expected,
						'account_id': line.analytic_account_id.id,
						'unit_amount': line.quantity_done,
						'amount': (line.product_id.standard_price *line.quantity_done) * -1,
						'product_id': line.purchase_line_id.product_id.id,
						'product_uom_id': line.purchase_line_id.product_uom.id,
						'general_account_id': self.partner_id.property_account_payable_id.id,
						'ref': ref,
						'tag_ids':[(6,0,tag_ids)]
					})
					self.env['account.analytic.line'].create(purchase_analytic_dict)

		if not self.purchase_id and not self.sale_id:
			for line in self.move_lines:
				if line.analytic_account_id:
					tag_ids =[]
					for tag_id in line.tag_ids:
						tag_ids.append(tag_id.id)  
					purchase_analytic_dict.update({
						'name': line.product_id.name,
						'date': datetime.now(),
						'account_id': line.analytic_account_id.id,
						'unit_amount': line.quantity_done ,
						'amount': line.product_id.lst_price * line.quantity_done ,
						'product_id': line.product_id.id,
						'product_uom_id': line.product_uom.id,
						'general_account_id': self.partner_id.property_account_receivable_id.id,
						'ref': ref,
					   'tag_ids':[(6,0,tag_ids)] 
					})
					if self.picking_type_id.code == 'incoming':
						purchase_analytic_dict['amount']= (line.product_id.standard_price *line.quantity_done) * -1 
							 
					self.env['account.analytic.line'].create(purchase_analytic_dict)
		return super(StockPicking, self).button_validate()


		
