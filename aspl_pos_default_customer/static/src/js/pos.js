odoo.define('aspl_pos_default_customer.pos', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    var DB = require('point_of_sale.DB');
    var chrome = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');

    chrome.Chrome.include({
        build_widgets: function(){
           var self = this;
           var partner = self.pos.config.partner_id;
           if(partner){
               var set_partner = self.pos.db.get_partner_by_id(partner[0])
                if(set_partner){
                    self.pos.get_order().set_client(set_partner);
                }
            } else if(self.pos && self.pos.get_order()){
               self.pos.get_order().set_client(null);
           }
           this._super();
        },
    });

    screens.ClientListScreenWidget.include({
        show: function(){
            var self = this;
            var order = this.pos.get_order();
            this._super();

            this.$('.default').click(function(){
                self.default_customer();
                self.gui.back();
            });
        },
        default_customer: function(){
            var order = this.pos.get_order();
            var self = this;
            if( this.has_client_changed() ){
                if (this.new_client) {
                    order.set_client(this.new_client);
                    var param_config = {
                        model: 'pos.config',
                        method: 'write',
                        args: [self.pos.config.id,{'partner_id':this.new_client.id}],
                    }
                    rpc.query(param_config, {async: false}).then(function(result){
                    }).fail(function(type,error){
                            if(error.data.message){
                                self.pos.db.notification('error',error.data.message);
                            }
                    });
                }
            }
        },
    });

});

