/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_product_exchange.pos_product_exchange', function (require) {
"use strict";
	var pos_orders = require('pos_orders.pos_orders');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var screens = require('point_of_sale.screens');
	var models = require('point_of_sale.models');
	var PopupWidget = require('point_of_sale.popups');
	var _t = core._t;
	var SuperOrder = models.Order;
	var SuperPosOrder =  pos_orders.prototype;	

	models.Order = models.Order.extend({
		initialize: function(attributes,options){
			var self = this;
			self.is_exchange_order = false;
			SuperOrder.prototype.initialize.call(this,attributes,options);
		},
	});


	var OrderExchangePopup = PopupWidget.extend({
		template: 'OrderExchangePopup',
		events: {
			'click .button.cancel':  'click_cancel',
			'click #complete_exchange':  'click_complete_exchange',
			'click #exchange_order':  'click_exchange_order',
		},
		click_exchange_order: function(){
			var self = this;
			var all = $('.exchange_qty');
			var return_dict = {};
			var return_entries_ok = true;
			$.each(all, function(index, value){
				var input_element = $(value).find('input');
				var line_quantity_remaining = parseFloat(input_element.attr('line-qty-remaining'));
				var line_id = parseFloat(input_element.attr('line-id'));
				var qty_input = parseFloat(input_element.val());
				if(!$.isNumeric(qty_input) || qty_input > line_quantity_remaining || qty_input < 0){
					return_entries_ok = false;
					input_element.css("background-color","#ff8888;");
					setTimeout(function(){
						input_element.css("background-color","");
					},100);
					setTimeout(function(){
						input_element.css("background-color","#ff8888;");
					},200);
					setTimeout(function(){
						input_element.css("background-color","");
					},300);
					setTimeout(function(){
						input_element.css("background-color","#ff8888;");
					},400);
					setTimeout(function(){
						input_element.css("background-color","");
					},500);
				}

				if(qty_input == 0 && line_quantity_remaining != 0 && !self.options.is_partial_return)
					self.options.is_partial_return = true;
				else if(qty_input > 0){
					return_dict[line_id] = qty_input;
					if(line_quantity_remaining != qty_input  && !self.options.is_partial_return)
						self.options.is_partial_return = true;
					else if(!self.options.is_partial_return)
						self.options.is_partial_return = false;
				}
			});
			if(return_entries_ok)
				self.create_return_order(return_dict);
		},
		create_return_order: function(return_dict){
			var self = this;
			var order = self.options.order;
			var orderlines = self.options.orderlines;
			var current_order = self.pos.get_order(); 
			if(Object.keys(return_dict).length > 0){
				self.chrome.widget.order_selector.neworder_click_handler();
				var refund_order = self.pos.get_order();
				refund_order.is_return_order = true;
				refund_order.is_exchange_order = true;
				refund_order.set_client(self.pos.db.get_partner_by_id(order.partner_id[0]));
				Object.keys(return_dict).forEach(function(line_id){
					var line = self.pos.db.line_by_id[line_id];
					var product = self.pos.db.get_product_by_id(line.product_id[0]);
					refund_order.add_product(product,{quantity:-1*parseFloat(return_dict[line_id]), price:line.price_unit,discount:line.discount});
					refund_order.selected_orderline.original_line_id = line.id;
				});
				if(self.options.is_partial_return){
					refund_order.return_status = 'Partially-Returned';
					refund_order.return_order_id = order.id;
				}else{
					refund_order.return_status = 'Fully-Returned';
					refund_order.return_order_id = order.id;
				}
				self.pos.set_order(refund_order);
				self.gui.show_screen('payment');				
				self.gui.show_screen('products');
			}
			else{
				self.$("input").css("background-color","#ff8888;");
				setTimeout(function(){
					self.$("input").css("background-color","");
				},100);
				setTimeout(function(){
					self.$("input").css("background-color","#ff8888;");
				},200);
				setTimeout(function(){
					self.$("input").css("background-color","");
				},300);
				setTimeout(function(){
					self.$("input").css("background-color","#ff8888;");
				},400);
				setTimeout(function(){
					self.$("input").css("background-color","");
				},500);
			}
		},
		click_complete_exchange: function(){
			var self = this;
			var all = $('.exchange_qty');
			$.each(all, function(index, value){
				var line_quantity_remaining = parseFloat($(value).find('input').attr('line-qty-remaining'));
				$(value).find('input').val(line_quantity_remaining);
			});
		},
		show: function(options){
			options = options || {};
			var self = this;
			this._super(options);
			this.orderlines = options.orderlines	|| [];
			this.renderElement();
		},
	});
	gui.define_popup({ name: 'exchange_products_popup', widget: OrderExchangePopup });
	
	pos_orders.include({
		events : _.extend({}, SuperPosOrder.events, {
            'click #wk_exchange': 'wk_exchange_order',
		}),
		wk_exchange_order: function(event){
			var self = this;
			var order_id = $('.wk-order-line.highlight').data('id');
			var order = self.pos.db.order_by_id[order_id];
			var all_pos_orders = self.pos.get('orders').models || [];
			var return_order_exist = _.find(all_pos_orders, function(pos_order){
				if(pos_order.return_order_id && pos_order.return_order_id == order_id)
					return pos_order;
					
			});
			if(return_order_exist){
				self.gui.show_popup('my_message',{
					'title': _t('Exchange/Return Already In Progress'),
					'body': _t("Exchange/Return order is already in progress. Please proceess with Order Reference " + return_order_exist.sequence_number),
				});
			}
			else if(order){
				var order_list = self.pos.db.pos_all_orders;
				var order_line_data = self.pos.db.pos_all_order_lines;
				var message = '';
				var non_returnable_products = false;
				var original_orderlines = [];
				var allow_return = true;
				if(order.return_status == 'Fully-Returned'){
					message = 'No items are left to return for this order!!'
					allow_return = false;
				}
				if (allow_return) {
					order.lines.forEach(function(line_id){
						var line = self.pos.db.line_by_id[line_id];
						var product = self.pos.db.get_product_by_id(line.product_id[0]);
						if(product == null){
							non_returnable_products = true;
							message = 'Some product(s) of this order are unavailable in Point Of Sale, do you wish to exchange other products?'
						}
						else if (product.not_returnable) {
							non_returnable_products = true;
							message = 'This order contains some Non-Returnable products, do you wish to exchange other products?'
						}
						else if(line.qty - line.line_qty_returned > 0)
							original_orderlines.push(line);
					});
					if(original_orderlines.length == 0){
						self.gui.show_popup('my_message',{
							'title': _t('Cannot exchange This Order!!!'),
							'body': _t("There are no exchangable products left for this order. Maybe the products are Non-Returnable or unavailable in Point Of Sale!!"),
						});
					}
					else if(non_returnable_products){
						self.gui.show_popup('confirm',{
							'title': _t('Warning !!!'),
							'body': _t(message),
							confirm: function(){
								self.gui.show_popup('exchange_products_popup',{
									'orderlines': original_orderlines,
									'order':order,
									'is_partial_return':true,
								});
							},
						});
					}
					else{
						self.gui.show_popup('exchange_products_popup',{
							'orderlines': original_orderlines,
							'order':order,
							'is_partial_return':false,
						});
					}
				}
				else
				{
					self.gui.show_popup('my_message',{
						'title': _t('Warning!!!'),
						'body': _t(message),
					});
				}
			}
		},
	});

});