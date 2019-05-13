# -*- coding: utf-8 -*-

from odoo import models,fields,api,_
from odoo.exceptions import Warning
class SubcontractOrder(models.Model):
    _name = 'subcontract.order'
    
    @api.one
    @api.depends('consubable_line_ids.cost','purchase_id')
    def _compute_consumed_product_cost(self):
        self.cost = sum(line.cost for line in self.consubable_line_ids) + self.purchase_id.amount_total or 0.0
        
    name = fields.Char("Name", default=lambda self: _('New'), index=True)
    start_date = fields.Datetime("Start Date")
    end_date = fields.Datetime("End Date")
    user_id = fields.Many2one("res.users",'Assigned User')
    partner_id = fields.Many2one("res.partner","Supplier")
    scheduled_date = fields.Datetime("Scheduled Date")
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],string='Status',default='draft')
    
    final_product_id = fields.Many2one("product.product","Product")
    uom_id = fields.Many2one("product.uom",'UOM')
    quantity = fields.Float("Quantity", default=1.0)
    cost = fields.Float("Cost",compute="_compute_consumed_product_cost",store=True)
    
    stock_out_picking_type_id = fields.Many2one('stock.picking.type','Stock-Out Operation Type')
    stock_in_picking_type_id = fields.Many2one('stock.picking.type','Stock-In Operation Type')
    s_location_id = fields.Many2one("stock.location","Subcontracting Location",domain=[('usage','=','transit')])
    m_location_id = fields.Many2one("stock.location","Material Location")
    
    order_line_ids = fields.One2many('subcontract.order.line','contract_id','Sub-Contract Lines')
    consubable_line_ids = fields.One2many('contract.consumable.matrerial','contract_id','Consumable Material Lines')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('subcontract.order'))
    purchase_id = fields.Many2one("purchase.order","Purchase Order")
     
    @api.onchange('final_product_id')
    def onchange_product_id(self):
        if self.final_product_id:
            self.uom_id = self.final_product_id.uom_po_id or self.final_product_id.uom_id
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('subcontract.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('subcontract.order') or _('New')
        result = super(SubcontractOrder, self).create(vals)
        return result
    @api.multi
    def action_view_purchase_order(self):
        if not self.purchase_id:
            raise Warning("Purchase order not created for this SubContract, please create it first.")
        if self.purchase_id.state=='draft':
            action = self.env.ref('purchase.purchase_rfq')
        else:
            action = self.env.ref('purchase.purchase_form_action')
        result = action.read()[0]
        
        res = self.env.ref('purchase.purchase_order_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = self.purchase_id.id
        return result
        
    
    @api.multi
    def action_view_picking(self):
        pickings = self.env['stock.picking'].search([('subcontract_id','=',self.id)])
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        if len(pickings) != 1:
            result['domain'] = "[('id', 'in', " + str(pickings.ids) + ")]"
        elif len(pickings) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pickings.id
        return result
    
    @api.multi
    def action_confirm_contract_order(self):
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        fields = picking_obj._fields.keys()
        if not self.purchase_id:
            self.action_create_purchase_order()
        #Receivable Movement Document
        vals = picking_obj.default_get(fields)
        vals.update({'subcontract_id':self.id,'picking_type_id':self.stock_in_picking_type_id.id,'location_id':self.s_location_id.id,'location_dest_id':self.m_location_id.id,})
        picking_rec = picking_obj.create(vals)
        
        move_line = move_obj.new({'product_id':self.final_product_id.id,'location_id':self.s_location_id.id,'location_dest_id':self.m_location_id.id,'price_unit':self.cost})
        move_line.onchange_product_id()
        move_vals = move_line._convert_to_write({name: move_line[name] for name in move_line._cache})
        move_vals.update({'picking_id':picking_rec.id,'product_uom_qty':self.quantity})
        move_obj.create(move_vals)
        
        #Consumable movement document
        vals = picking_obj.default_get(fields)
        vals.update({'subcontract_id':self.id,'picking_type_id':self.stock_out_picking_type_id.id,'location_id':self.m_location_id.id,'location_dest_id':self.s_location_id.id,})
        picking_rec = picking_obj.create(vals)
        
        for line in self.consubable_line_ids:
            move_line = move_obj.new({'product_id':line.product_id.id,'location_id':self.m_location_id.id,'location_dest_id':self.s_location_id.id,'price_unit':line.cost})
            move_line.onchange_product_id()
            move_vals = move_line._convert_to_write({name: move_line[name] for name in move_line._cache})
            move_vals.update({'picking_id':picking_rec.id,'product_uom_qty':line.quantity})
            move_obj.create(move_vals)
        self.write({'state':'confirmed'})
        return True
    
    @api.multi
    def action_create_purchase_order(self):
        if self.purchase_id:
            raise Warning("Purchase order already created for this SubContract.")
        
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        purchase_vals = purchase_obj.default_get(['date_order','invoice_status','picking_type_id','company_id'])
        purchase_vals.update({'partner_id':self.partner_id.id,})
        purchase = purchase_obj.new(purchase_vals)
        purchase.onchange_partner_id()
        purchase_vals = purchase._convert_to_write({name: purchase[name] for name in purchase._cache})
        purchase_rec = purchase_obj.create(purchase_vals)
        for line in self.order_line_ids:
            purchase_line = purchase_line_obj.new({'product_id':line.product_id.id,'product_qty':line.quantity})
            purchase_line.onchange_product_id()
            purchase_line_vals = purchase_line._convert_to_write({name: purchase_line[name] for name in purchase_line._cache})
            purchase_line_vals.update({'order_id':purchase_rec.id})
            purchase_line_obj.create(purchase_line_vals)
        self.write({'purchase_id':purchase_rec.id})
        
        action = self.env.ref('purchase.purchase_rfq')
        result = action.read()[0]
        
        res = self.env.ref('purchase.purchase_order_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = purchase_rec.id
        return result
        
    
class SubcontractOrderLine(models.Model):
    _name = 'subcontract.order.line'
    
    product_id = fields.Many2one("product.product","Product")
    name = fields.Char("Description")
    account_analytic_id = fields.Many2one('account.analytic.account','Analytic Account')
    quantity = fields.Float("Quantity", default=1.0)
    uom_id = fields.Many2one("product.uom",'UOM')
    contract_id = fields.Many2one("subcontract.order",'Sub-Contract')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name_get()[0][1]
            self.uom_id = self.product_id.uom_po_id or self.product_id.uom_id
            
class ContractConsumableMaterial(models.Model):
    _name = 'contract.consumable.matrerial'
    
    product_id = fields.Many2one("product.product","Product")
    quantity = fields.Float("Quantity", default=1.0)
    uom_id = fields.Many2one("product.uom",'UOM')
    cost = fields.Float("Cost")
    contract_id = fields.Many2one("subcontract.order",'Sub-Contract')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.cost = self.product_id.standard_price
            self.uom_id = self.product_id.uom_po_id or self.product_id.uom_id
            