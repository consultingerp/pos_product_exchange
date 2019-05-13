// pos_logo_change js
odoo.define('de_pos_receipt.pos',function(require){
	"use strict";
	var models = require('point_of_sale.models');
	var chrome=require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var popups = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    var _t = core._t;


    var _super_posmodel = models.PosModel.prototype;
    console.log("---1---",_super_posmodel)
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var company_model = _.find(this.models, function(model){ return model.model === 'res.company'; });
            company_model.fields.push('logo','street','city','state_id');
            // Push Other fields of res.company so we can access those fields in
            // POS...
            return _super_posmodel.initialize.call(this, session, attributes);
        },
        
    });

//    var _super_order = models.Order.prototype;
//    models.Order = models.Order.extend({
//        validate_order: function(){
//            new Model("pos.order").call('create_new_job', {}, {async: false})
//            .then(function(result){
//                if(result){
//                    order.set_job_created_name(result);
//                }
//            });
//        }
//    });



//    args: [from, to, category, limit, self.pos.pos_session.id, current_session_report],

// chrome.OrderSelectorWidget.include({
// init: function(parent, options) {
// this._super(parent, options);
// this.pos.get('orders').bind('add remove change',this.renderElement,this);
// this.pos.bind('change:selectedOrder',this.renderElement,this);
//		    
// //this custom code is for pos_logo
// var $image = self.$('#pos-logo');
// $image.attr("src",'/web/image?model=pos.config&field=pos_logo&id='+this.pos.config.id);
// $image.css( { marginLeft : "15px", marginTop : "5px", 'border-radius':'3px' }
// ); //width:'100px',
// },
// });




});;
