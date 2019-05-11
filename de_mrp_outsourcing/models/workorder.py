from datetime import datetime
from odoo import models,fields,api
from odoo.exceptions import Warning

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_subcontracting = fields.Boolean('Is Subcontracting')

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    purchase_id = fields.Many2one('purchase.order', 'Purchase')
    delivery_id = fields.Many2one('stock.picking', 'Delivery')
    return_id = fields.Many2one('stock.picking', 'Return')
    is_subcontracting = fields.Boolean(related='workcenter_id.is_subcontracting', string='Is Subcontracting', store=True)

    @api.multi
    def create_subcontracting(self):
        for workorder_rec in self:
            #Raising Various Warnings
            partner_rec = workorder_rec.workcenter_id.partner_id
            if not partner_rec:
                raise Warning("There is no Partner defined in Workcenter '%s' for Subcontracting."%(workorder_rec.workcenter_id.name))
            produce_product_rec = workorder_rec.product_id
            product_rec = workorder_rec.workcenter_id.service_product_id
            if not product_rec:
                raise Warning("There is no Product defined in Workcenter '%s' for Subcontracting."%(workorder_rec.workcenter_id.name))
            delivery_type_rec = workorder_rec.workcenter_id.delivery_type_id
            if not delivery_type_rec:
                raise Warning("There is no Delivery Type defined in Workcenter '%s' for Subcontracting."%(workorder_rec.workcenter_id.name))
            return_type_rec = workorder_rec.workcenter_id.return_type_id
            if not return_type_rec:
                raise Warning("There is no Return Type defined in Workcenter '%s' for Subcontracting." % (
                workorder_rec.workcenter_id.name))

            #Creating Purchase Order Vals
            purchase_vals = {
                'partner_id': partner_rec.id,
                'company_id': self.env.user.company_id.id,
                'currency_id': partner_rec.property_purchase_currency_id.id or self.env.user.company_id.currency_id.id,
                'origin': workorder_rec.production_id.name,
                'payment_term_id': partner_rec.property_supplier_payment_term_id.id,
                'date_order': str(datetime.now()),
                'is_subcontracting': True,
            }
            purchase_rec = self.env['purchase.order'].create(purchase_vals)
            workorder_rec.purchase_id = purchase_rec.id

            #Creating Purchase Order Line Vals
            line_data = {
                'name': product_rec.name,
                'product_qty': workorder_rec.qty_production,
                'product_id': product_rec.id or False,
                'product_uom': product_rec.uom_po_id.id,
                'price_unit': workorder_rec.workcenter_id.cost_per_qty or 0.0,
                'company_id': self.env.user.company_id.id,
                'order_id': purchase_rec.id,
                'date_planned': str(datetime.now())
            }
            self.env['purchase.order.line'].create(line_data)

            #Creating Delivery Picking Vals
            delivery_vals = {
                'picking_type_id': delivery_type_rec.id,
                'partner_id': partner_rec.id,
                'date': str(datetime.now()),
                'origin': workorder_rec.production_id.name,
                'location_dest_id': partner_rec.property_stock_supplier.id,
                'location_id': partner_rec.property_stock_supplier.id,
                'company_id': self.env.user.company_id.id,
            }
            delivery_rec = self.env['stock.picking'].create(delivery_vals)

            # Creating the stock move vals
            stock_move_vals = {
                'name': delivery_rec.name or '',
                'product_id': produce_product_rec.id,
                'product_uom': produce_product_rec.uom_po_id.id,
                'date': str(datetime.now()),
                'date_expected': str(datetime.now()),
                'location_id': partner_rec.property_stock_supplier.id,
                'location_dest_id': partner_rec.property_stock_supplier.id,
                'partner_id': partner_rec.id,
                'state': 'draft',
                'company_id': self.env.user.company_id.id,
                'price_unit': workorder_rec.workcenter_id.cost_per_qty or 0.0,
                'origin': workorder_rec.production_id.name,
                'product_uom_qty': workorder_rec.qty_production
            }
            stock_move_vals.update({
                'picking_type_id': delivery_type_rec.id,
                'picking_id': delivery_rec.id
            })
            self.env['stock.move'].create(stock_move_vals)
            workorder_rec.delivery_id = delivery_rec.id

            #Creating the Return Picking Vals
            return_vals = {
                'picking_type_id': return_type_rec.id,
                'partner_id': partner_rec.id,
                'date': str(datetime.now()),
                'origin': workorder_rec.production_id.name,
                'location_dest_id': partner_rec.property_stock_supplier.id,
                'location_id': partner_rec.property_stock_supplier.id,
                'company_id': self.env.user.company_id.id,
            }
            return_rec = self.env['stock.picking'].create(return_vals)
            stock_move_vals.update({
                'picking_type_id': return_type_rec.id,
                'picking_id': return_rec.id
            })
            self.env['stock.move'].create(stock_move_vals)
            workorder_rec.return_id = return_rec.id
        return True
