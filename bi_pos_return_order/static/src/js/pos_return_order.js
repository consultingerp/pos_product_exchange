// pos_return_order js
odoo.define('bi_pos_return_order.pos', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    //var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var field_utils = require('web.field_utils');
    var pos_orders_list = require('pos_orders_list.pos_orders_list');

    var _t = core._t;



	 // pos_orders_list start

    pos_orders_list.include({
        
        show: function(options) {
            var self = this;
            this._super(options);

            this.details_visible = false;

            var orders = self.pos.db.all_orders_list;
            //console.log("***************************************ordersssssssssssssss",orders)
            this.render_list_orders(orders, undefined);

	    	this.$('.back').click(function(){
		        //self.gui.back();
		        self.gui.show_screen('products');
            });
            
            //Return Order
            this.$('.orders-list-contents').delegate('.return-order', 'click', function(result) {
                var order_id = parseInt(this.id);
                var selectedOrder = null;
		        for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
		            if (orders[i] && orders[i].id == order_id) {
		                selectedOrder = orders[i];
		            }
		        }
		        
                var orderlines = [];
            	var order_list = self.pos.db.all_orders_list;
                var order_line_data = self.pos.db.all_orders_line_list;

                selectedOrder.lines.forEach(function(line_id) {
		            var line = self.pos.db.get_lines_by_id[line_id];
		            var product = self.pos.db.get_product_by_id(line.product_id[0]);
		            orderlines.push(line);
                });

            	self.gui.show_popup('pos_return_order_popup_widget', { 'orderlines': orderlines, 'order': selectedOrder });
            });
            //End Return Order

        },
        //
	});
    // End pos_orders_list




    // Popup start

    var PosReturnOrderPopupWidget = popups.extend({
        template: 'PosReturnOrderPopupWidget',
        init: function(parent, args) {
            this._super(parent, args);
            this.options = {};
        },
        //
        show: function(options) {
        	options = options || {};
        	//console.log("optionssssssssssssssssssssssssssssssssssssssssssssssssssss",options)
            var self = this;
            this._super(options);
            this.orderlines = options.orderlines || [];
            //console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!this.orderlines",this.orderlines)

        },
        //
        renderElement: function() {
            var self = this;
            this._super();
            var selectedOrder = this.pos.get_order();
            var orderlines = self.options.orderlines;
            var order = self.options.order;

			var return_products = {};
			var exact_return_qty = {};
            		var exact_entered_qty = {};



            this.$('#apply_return_order').click(function() {
                var entered_code = $("#entered_item_qty").val();
                var list_of_qty = $('.entered_item_qty');


				$.each(list_of_qty, function(index, value) {
				 	var entered_item_qty = $(value).find('input');
               	    var qty_id = parseFloat(entered_item_qty.attr('qty-id'));
		            var line_id = parseFloat(entered_item_qty.attr('line-id'));
		            var entered_qty = parseFloat(entered_item_qty.val());
		            
		            exact_return_qty = qty_id;
                    exact_entered_qty = entered_qty || 0;

		            if(!exact_entered_qty){
		            	return;
                    }
                    else if (exact_return_qty >= exact_entered_qty){
		              return_products[line_id] = entered_qty;
                    }
                    else{
                    alert("Cannot Return More quantity than purchased")
                    }

            	});
            	//return return_products;


            	Object.keys(return_products).forEach(function(line_id) {
            		var line = self.pos.db.get_lines_by_id[line_id];
                	var product = self.pos.db.get_product_by_id(line.product_id[0]);
                	
                	selectedOrder.add_product(product, {
                        quantity: - parseFloat(return_products[line_id]),
                        price: line.price_unit,
                        discount: line.discount
                    });
                    selectedOrder.selected_orderline.original_line_id = line.id;
            	});
            	self.pos.set_order(selectedOrder);
            	self.gui.show_screen('products');

               });

        },

    });
    gui.define_popup({
        name: 'pos_return_order_popup_widget',
        widget: PosReturnOrderPopupWidget
    });

    // End Popup start





});
