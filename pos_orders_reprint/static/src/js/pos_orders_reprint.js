// pos_orders_reprint js
//console.log("custom callleddddddddddddddddddddd")
odoo.define('pos_orders_reprint.pos_orders_reprint', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var ActionManagerBrowseinfo = require('web.ActionManager');
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var pos_orders_list = require('pos_orders_list.pos_orders_list');

    var _t = core._t;

 var ReceiptScreenWidgetNew = screens.ScreenWidget.extend({
       template: 'ReceiptScreenWidgetNew',
        show: function() {
            var self = this;
            self._super();
            $('.button.back').on("click", function() {
                self.gui.show_screen('see_all_orders_screen_widget');
            });
            $('.button.print').click(function() {
                var test = self.chrome.screens.receipt;
                setTimeout(function() { self.chrome.screens.receipt.lock_screen(false); }, 1000);
                if (!test['_locked']) {
                    self.chrome.screens.receipt.print_web();
                    self.chrome.screens.receipt.lock_screen(true);
                }
            });
        }
    });
    gui.define_screen({ name: 'ReceiptScreenWidgetNew', widget: ReceiptScreenWidgetNew });


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
            
            this.$('.orders-list-contents').delegate('.print-order', 'click', function(result) {
                //console.log("clikckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkked")
                var order_id = parseInt(this.id);
                var orderlines = [];
		        var paymentlines = [];
		        var discount = 0;
		        var subtotal = 0;
		        var tax = 0;
                //console.log("order_iddddddddddddddddddddddddddddddddddddddddd",order_id)

                var selectedOrder = null;
		        for(var i = 0, len = Math.min(orders.length,1000); i < len; i++) {
		            if (orders[i] && orders[i].id == order_id) {
		                selectedOrder = orders[i];
		                //console.log("selectedOrder_newewwwwwwwwwwwwwwwwwwwwwwwwwwwww",selectedOrder)
		            }
		        }

            //if (self.pos.config.pos_order_reprint == 'ticket') {
                
		            rpc.query({
				        model: 'pos.order',
				        method: 'print_pos_receipt',
				        args: [order_id],
		            
		            }).then(function(output) {
		            
                

                    //console.log("outputttttttttttttttttttttt", output)
		            //var selectedOrder = self.pos.get('selectedOrder');
					//console.log("order_iddddddddddddddddddddddddddddddddddddddddd",selectedOrder)

					orderlines = output[0];
		            paymentlines = output[2];
		            discount = output[1];
		            subtotal = output[4];
		            tax = output[5];
		            self.gui.show_screen('ReceiptScreenWidgetNew');
		            $('.pos-receipt-container').html(QWeb.render('PosTicket1',{
		                widget:self,
		                order: selectedOrder,
		                paymentlines: paymentlines,
		                orderlines: orderlines,
		                discount_total: discount,
		                change: output[3],
		                subtotal: subtotal,
		                tax: tax,
		            }));


				});
			//}

        });

        },
        //
	});
	
	

});
