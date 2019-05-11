odoo.define('de_double_print.screens', function (require) {	
	var core = require('web.core');
    var QWeb = core.qweb;
	var pos_screens = require('point_of_sale.screens');
	pos_screens.ReceiptScreenWidget.include({
		print_web: function() {
			console.log(8888823);
			//window.print();	
			window.print();	
			setTimeout(window.print(),2000);			
			this.pos.get_order()._printed = true;		
		},
		print_xml: function() {
			
			var receipt = QWeb.render('XmlReceipt', this.get_receipt_render_env());
			this.pos.proxy.print_receipt(receipt);
			//console.log(123);
			//this.pos.proxy.print_receipt(receipt);
			
			this.pos.get_order()._printed = true;
		},
	});
});