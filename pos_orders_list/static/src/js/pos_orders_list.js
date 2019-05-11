// pos_orders_list js
//console.log("custom callleddddddddddddddddddddd")
odoo.define('pos_orders_list.pos_orders_list', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var QWeb = core.qweb;

    var _t = core._t;


// Load Models here...

    models.load_models({
        model: 'pos.order',
        fields: ['name', 'id', 'date_order', 'partner_id', 'pos_reference', 'lines', 'amount_total', 'session_id', 'state', 'company_id'],
        domain: null,
        loaded: function(self, orders){
        	//console.log("111111111111loadedddddddddddddddddddddddddddddddddddd",orders);
        	self.db.all_orders_list = orders;
        	//console.log("111111111111loadedddddddddddddddddddddddddddddddddddd",orders);
        	
        	self.db.get_orders_by_id = {};
            orders.forEach(function(order) {
                self.db.get_orders_by_id[order.id] = order;
            });
            
            self.orders = orders;
            //console.log("***************orderssssssssssssssssssssssss", orders);
        },
    });

    models.load_models({
        model: 'pos.order.line',
        fields: ['order_id', 'product_id', 'discount', 'qty', 'price_unit'],
        domain: function(self) {
            var order_lines = []
            var orders = self.db.all_orders_list;
            for (var i = 0; i < orders.length; i++) {
                order_lines = order_lines.concat(orders[i]['lines']);
            }
            return [
                ['id', 'in', order_lines]
            ];
        },
        loaded: function(self, pos_order_line) {
            self.db.all_orders_line_list = pos_order_line;
            self.db.get_lines_by_id = {};
            pos_order_line.forEach(function(line) {
                self.db.get_lines_by_id[line.id] = line;
            });

            self.pos_order_line = pos_order_line;
        },
    });

    

    // SeeAllOrdersScreenWidget start

    var SeeAllOrdersScreenWidget = screens.ScreenWidget.extend({
        template: 'SeeAllOrdersScreenWidget',
        init: function(parent, options) {
            this._super(parent, options);
            //this.options = {};
        },
        //
        
        line_selects: function(event,$line,id){
        	//console.log('calllllllll',id);
        	var self = this;
            var orders = this.pos.db.get_orders_by_id[id];
            //console.log("line select orderssssssssssssssssssssssssssssssssssssss", orders);
            this.$('.client-list .lowlight').removeClass('lowlight');
            if ( $line.hasClass('highlight') ){
                $line.removeClass('highlight');
                $line.addClass('lowlight');
                this.display_orders_detail('hide',orders);
                this.new_clients = null;
                //this.toggle_save_button();
            }else{
                this.$('.client-list .highlight').removeClass('highlight');
                $line.addClass('highlight');
                var y = event.pageY - $line.parent().offset().top;
                this.display_orders_detail('show',orders,y);
                this.new_clients = orders;
                //this.toggle_save_button();
            }
            
        },
        
        display_orders_detail: function(visibility,order,clickpos){
            var self = this;
            var contents = this.$('.client-details-contents');
            var parent   = this.$('.orders-line ').parent();
            var scroll   = parent.scrollTop();
            var height   = contents.height();

            contents.off('click','.button.edit');
            contents.off('click','.button.save');
            contents.off('click','.button.undo');

            this.editing_client = false;
            this.uploaded_picture = null;

            if(visibility === 'show'){
                contents.empty();
                //console.log('ssssssssssssssssssss',visibility);
                contents.append($(QWeb.render('OrderDetails',{widget:this,order:order})));

                var new_height   = contents.height();

                if(!this.details_visible){
                    if(clickpos < scroll + new_height + 20 ){
                        parent.scrollTop( clickpos - 20 );
                    }else{
                        parent.scrollTop(parent.scrollTop() + new_height);
                    }
                }else{
                    parent.scrollTop(parent.scrollTop() - height + new_height);
                }

                this.details_visible = true;
                //this.toggle_save_button();
            } else if (visibility === 'hide') {
                //console.log('sssssssshhhhhhhssssssssssss hideeeeeeeeeeeeeeeeeeeeeeeeeeeeee',visibility);
                contents.empty();
                if( height > scroll ){
                    contents.css({height:height+'px'});
                    contents.animate({height:0},400,function(){
                        contents.css({height:''});
                    });
                }else{
                    parent.scrollTop( parent.scrollTop() - height);
                }
                this.details_visible = false;
                //this.toggle_save_button();
            }
        },
        
        get_selected_partner: function() {
            var self = this;
            if (self.gui)
                return self.gui.get_current_screen_param('selected_partner_id');
            else
                return undefined;
        },
        
        render_list_orders: function(orders, search_input){
            var self = this;
            var selected_partner_id = this.get_selected_partner();
            //console.log("<<<<<<<<<<<<<<<<<<<<<<<selected_partner_id>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",selected_partner_id)
            var selected_client_orders = [];
            if (selected_partner_id != undefined) {
                for (var i = 0; i < orders.length; i++) {
                    if (orders[i].partner_id[0] == selected_partner_id)
                        selected_client_orders = selected_client_orders.concat(orders[i]);
                }
                orders = selected_client_orders;
                //console.log("upar orderssssssssssssssssssssssssssssss",orders)
            }
            
           if (search_input != undefined && search_input != '') {
                var selected_search_orders = [];
                var search_text = search_input.toLowerCase()
                //console.log("111111111111111111111111query",search_text)
                for (var i = 0; i < orders.length; i++) {
                    if (orders[i].partner_id == '') {
                        orders[i].partner_id = [0, '-'];
                    }
                    //console.log("111111111111111111111111query",search_text
                    if (((orders[i].name.toLowerCase()).indexOf(search_text) != -1) || ((orders[i].partner_id[1].toLowerCase()).indexOf(search_text) != -1) || ((orders[i].pos_reference.toLowerCase()).indexOf(search_text) != -1)) {
                        selected_search_orders = selected_search_orders.concat(orders[i]);
                        //console.log("1111111111111111111111111111new_order_data ",new_order_data)
                    }
                }
                orders = selected_search_orders;
                //console.log("upar orderssssssssssssssssssssssssssssss",orders)
            }
            
            
            //console.log("orderssssssssssssssssssssssssssssss",orders)
            var content = this.$el[0].querySelector('.orders-list-contents');
	        //console.log("contentssssssssssssssssssssss", content);
	        content.innerHTML = "";
	        var orders = orders;
	        //console.log("contentssssssssssssssssssssss", orders);
            for(var i = 0, len = Math.min(orders.length,1000); i < len; i++){
                var order    = orders[i];
                //console.log("1111111111111 contentssssssssssssssssssssss", order);
                var ordersline_html = QWeb.render('OrdersLine',{widget: this, order:orders[i], selected_partner_id: orders[i].partner_id[0]});
                var ordersline = document.createElement('tbody');
                ordersline.innerHTML = ordersline_html;
                ordersline = ordersline.childNodes[1];
                content.appendChild(ordersline);

            }
        },
        //
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
            
            //this code is for click on order line & that order will be appear 
            
            //this.$('.orders-list-contents').delegate('.orders-line', 'click', function(event) {
            //    self.line_selects(event, $(this), parseInt($(this).data('id')));
            //});
            
            
            //this code is for Search Orders
            this.$('.search-order input').keyup(function() {
                //console.log("***************************************ordersssssssssssssss",this.value)
                self.render_list_orders(orders, this.value);
            });
		    
		    
            
        },
        //
               

    });
    gui.define_screen({
        name: 'see_all_orders_screen_widget',
        widget: SeeAllOrdersScreenWidget
    });

    // End SeeAllOrdersScreenWidget
    
    

	// Start SeeAllOrdersButtonWidget
	
    var SeeAllOrdersButtonWidget = screens.ActionButtonWidget.extend({
        template: 'SeeAllOrdersButtonWidget',

        button_click: function() {
            var self = this;
            this.gui.show_screen('see_all_orders_screen_widget', {});
        },
        
    });

    screens.define_action_button({
        'name': 'See All Orders Button Widget',
        'widget': SeeAllOrdersButtonWidget,
        'condition': function() {
            return true;
        },
    });
    // End SeeAllOrdersButtonWidget	

// Start ClientListScreenWidget
		gui.Gui.prototype.screen_classes.filter(function(el) { return el.name == 'clientlist'})[0].widget.include({
            show: function(){
		        this._super();
		        var self = this;
		        this.$('.view-orders').click(function(){
		        	//console.log("callledddddddddddddddddddddddddddddddddddddddddd all orderssssssssssss")
            		self.gui.show_screen('see_all_orders_screen_widget', {});
            	});
            
            
            $('.selected-client-orders').on("click", function() {
                self.gui.show_screen('see_all_orders_screen_widget', {
                    'selected_partner_id': this.id
                });
            });
            
        },
    });
    
	return SeeAllOrdersScreenWidget;
});
