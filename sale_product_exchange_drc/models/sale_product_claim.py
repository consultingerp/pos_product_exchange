# -*- coding: utf-8 -*-
from openerp import api, fields, models
from openerp.exceptions import except_orm


class ProductSaleClaim(models.Model):
    _name = 'sale.claim'
    _description = 'Claim'
    _order = 'name desc'
    _inherit = ['mail.thread']

    name = fields.Char('Claim ID #', default='/', readonly=True)
    claim_sub = fields.Char('Claim Subject')
    saleorder_id = fields.Many2one('sale.order', string='Sale Order')
    state = fields.Selection([('new', 'New'),
                              ('progress', 'In-Progress'),
                              ('done', 'Done')],
                             compute='_get_claim_state', store=True, default='new')

    @api.depends('replace_delivery_picking_id.state', 'return_picking_id.state', 'confirmed', 'paid')
    def _get_claim_state(self):
        for claim in self:
            claim.state = 'new'
            if claim.return_type == 'credit_return':
                if claim.paid:
                    claim.state = 'done'
                elif claim.confirmed:
                    claim.state = 'progress'
            else:
                if claim.delivered:
                    claim.state = 'done'
                elif claim.confirmed:
                    claim.state = 'progress'

    group_id = fields.Many2one('procurement.group', compute='_get_procurement_group', store=True)

    @api.depends('saleorder_id')
    def _get_procurement_group(self):
        for claim in self:
            claim.group_id = claim.saleorder_id.procurement_group_id

    return_type = fields.Selection([('repair', 'Repair'),
                                    ('exchange', 'Exchange'),
                                    ('credit_return', 'Credit Return')], string='Return Type')
    partner_id = fields.Many2one('res.partner', string='Customer')
    return_picking_id = fields.Many2one('stock.picking')
    picking_ids = fields.One2many('stock.picking', 'claim_id')
    damage_location = fields.Many2one('stock.location', string='Damage Location',
                                      default=lambda self: self._get_default_damage_location())
    confirmed = fields.Boolean('Confirmed')
    received = fields.Boolean('Received')
    invoiced = fields.Boolean('Invoiced')
    paid = fields.Boolean('Paid', compute='_get_refund_invoice_state', store=True)

    @api.depends('invoice_ids.state')
    def _get_refund_invoice_state(self):
        for claim in self:
            claim.paid = False
            if claim.invoice_ids:
                invoice_paid = True
                for invoice in claim.invoice_ids:
                    if invoice.state != 'paid':
                        invoice_paid = False
                if invoice_paid:
                    claim.paid = True

    delivered = fields.Boolean('Delivered', compute='_get_delivered_state', store=True)

    @api.depends('replace_delivery_picking_id.state')
    def _get_delivered_state(self):
        for claim in self:
            if claim.replace_delivery_picking_id and \
                    claim.replace_delivery_picking_id.state == 'done':
                    claim.delivered = True
                    #Incoming Return from Customer
                    if claim.return_type =='exchange':
                        return_total = sum(each_move.product_id.lst_price * each_move.quantity_done for each_move in claim.return_picking_id.move_lines)
                        # Outgoing Shipment to Customer
                        replace_total = sum(each_move.product_id.lst_price * each_move.quantity_done for each_move in claim.replace_delivery_picking_id.move_lines)
                        if return_total == replace_total:
                            break
                        return_sign = -1 if replace_total > return_total else 1
                        replace_sign = 1 if replace_total > return_total else -1
                        type = 'out_invoice' if replace_total > return_total else 'out_refund'
                        invoice_line_ids = []
                        order_inv = claim.saleorder_id.order_line.mapped('invoice_lines').mapped('invoice_id')
                        for each_move in claim.return_picking_id.move_lines:
                            invoice_line_ids.append((0, 0, {'name': each_move.product_id.name, 'product_id': each_move.product_id.id,
                                                         'quantity': each_move.quantity_done, 'uom_id': each_move.product_id.uom_id.id,
                                                         'price_unit': each_move.product_id.lst_price * return_sign,
                                                         'account_id': each_move.product_id.categ_id.property_account_income_categ_id.id}))
                        for each_move in claim.replace_delivery_picking_id.move_lines:
                            invoice_line_ids.append((0, 0, {'name': each_move.product_id.name, 'product_id': each_move.product_id.id,
                                                         'quantity': each_move.quantity_done, 'uom_id': each_move.product_id.uom_id.id,
                                                         'price_unit': each_move.product_id.lst_price * replace_sign,
                                                         'account_id': each_move.product_id.categ_id.property_account_income_categ_id.id}))
                        invoice_vals = {
                            'name': '',
                            'type': type,
                            'partner_id': claim.partner_id.id,
                            'invoice_line_ids':invoice_line_ids,
                            'account_id': order_inv.account_id.id,
                            'journal_id': order_inv.journal_id.id,
                            'currency_id': order_inv.currency_id.id,
                            'claim_id': claim.id
                        }
                        self.env['account.invoice'].create(invoice_vals)

    replace_delivery_picking_id = fields.Many2one('stock.picking')
    claim_desc = fields.Text('Description')
    line_ids = fields.One2many('sale.claim.line', 'claim_id')
    picking_count = fields.Integer('Picking Count', compute='_calc_picking_count')

    @api.depends('picking_ids')
    def _calc_picking_count(self):
        for claim in self:
            claim.picking_count = claim.picking_ids and len(claim.picking_ids) or 0

    invoice_ids = fields.One2many('account.invoice', 'claim_id')
    total_invoices = fields.Float('Invoice Count', compute='_calc_invoice_count')

    @api.depends('invoice_ids')
    def _calc_invoice_count(self):
        for claim in self:
            claim.total_invoices = claim.invoice_ids and len(claim.invoice_ids) or 0

    # Constraints
    @api.constrains('saleorder_id')
    def _check_saleorder_duplication(self):
        for claim in self:
            claim_exists = claim.search([('saleorder_id', '=', claim.saleorder_id.id), ('id', '!=', claim.id)], limit=1)
            if claim_exists:
                raise except_orm('Claim already created for ' + claim.saleorder_id.name, claim_exists.name)

    def _get_default_damage_location(self):
        return self.env.ref('sale_product_exchange_drc.stock_location_damaged').id

    @api.multi
    def action_view_picking(self):
        for claim in self:
            return {
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window',
                'context': self._context,
                'domain': [('id', 'in', claim.picking_ids.ids)]
            }

    @api.onchange('saleorder_id')
    def _onchange_sale_order(self):
        self.partner_id = self.saleorder_id.partner_id.id

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id.id != self.saleorder_id.partner_id.id:
            self.saleorder_id = False

    # @api.onchange('saleorder_id')
    # def _onchange_sale_order(self):
    #     for claim in self:
    #         if claim.saleorder_id:
    #             res = []
    #             for line in claim.saleorder_id.order_line:
    #                 res.append((0, 0, {
    #                     'product_id': line.product_id.id,
    #                     'claim_id': claim.id,
    #                     'ordered_qty': line.product_uom_qty,
    #                     'uom_id': line.product_uom.id,
    #                 }
    #                             ))
    #             if res:
    #                 claim.line_ids = res

    @api.multi
    def fetch_products(self):
        for claim in self:
            claim.line_ids = False
            if claim.saleorder_id:
                res = []
                for line in claim.saleorder_id.order_line:
                    res.append((0, 0, {
                        'product_id': line.product_id.id,
                        'claim_id': claim.id,
                        'ordered_qty': line.product_uom_qty,
                        'uom_id': line.product_uom.id,
                    }
                                ))
                if res:
                    claim.line_ids = res

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get('sale.claim') or '/'
        res = super(ProductSaleClaim, self).create(vals)
        return res

    @api.multi
    def claim_confirm(self):
        for claim in self:
            for line in self.line_ids:
                if line.return_qty <= 0:
                    raise except_orm("Error!", "Can not return zero/negative quantity")
                if line.ordered_qty < line.return_qty:
                    raise except_orm("Error!", "Can not return quantity more then ordered quantity")
            claim.confirmed = True
            claim.saleorder_id.is_claim_created = True

    @api.multi
    def create_in_shipment(self):
        StockMove = self.env['stock.move']
        for claim in self:
            if claim.return_picking_id:
                raise except_orm('Incoming Shipment is Already created for this claim',
                                 'Shipment id is ' + claim.return_picking_id.name)
            pick_type_id = claim.saleorder_id.picking_ids and self.saleorder_id.picking_ids[0].picking_type_id and \
                           claim.saleorder_id.picking_ids[0].picking_type_id.return_picking_type_id.id
            destination_location = claim.saleorder_id.picking_ids[0].location_dest_id.id
            new_picking = claim.saleorder_id.picking_ids[0].copy({
                'move_lines': [],
                'picking_type_id': pick_type_id,
                'state': 'draft',
                'origin': claim.saleorder_id.name + ' - ' + claim.name,
                'claim_id': claim.id
            })

            claim.return_picking_id = new_picking.id
            for line in claim.line_ids:
                StockMove.create({
                    'name': line.product_id.product_tmpl_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.return_qty,
                    'product_uom': line.uom_id.id,
                    'picking_id': new_picking.id,
                    'state': 'draft',
                    'location_id': destination_location,
                    'location_dest_id': claim.damage_location.id,
                    'picking_type_id': pick_type_id,
                    'warehouse_id': claim.saleorder_id.warehouse_id.id,
                    'procure_method': 'make_to_stock',
                })

            if claim.return_type == 'credit_return':
                new_picking.invoice_state = '2binvoiced'
            else:
                new_picking.invoice_state = 'none'
            claim.received = True
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window',
                'res_id': new_picking.id,
                'context': self._context,
                'target': 'new',
                'flags': {'action_buttons': True}
            }

    @api.multi
    def open_refund_invoice(self):
        action_id = self.env.ref('account.action_invoice_tree2')
        if action_id:
            action = action_id.read()
            action = action[0] or action
            action['domain'] = "[('id','in', [" + ','.join(map(str, self.invoice_ids.ids)) + "])]"
            return action

    @api.multi
    def create_claim_refund_invoice(self):
        for claim in self:
            order_inv = claim.saleorder_id.order_line.mapped('invoice_lines').mapped('invoice_id')
            order_inv_lines = claim.saleorder_id.order_line.mapped('invoice_lines')
            invoice_vals = {
                'name': '',
                'type': 'out_refund',
                'partner_id': claim.partner_id.id,
                'invoice_line_ids': [(0, 0, {'name': line.product_id.name, 'product_id': line.product_id.id,
                                             'quantity': line.return_qty, 'uom_id': line.product_id.uom_id.id,
                                             'price_unit': line.product_id.standard_price,
                                             'account_id': order_inv.account_id.id}) for line in claim.line_ids],
                'account_id': order_inv.account_id.id,
                'journal_id': order_inv.journal_id.id,
                'currency_id': order_inv.currency_id.id,
                'claim_id': claim.id
            }
            inv = self.env['account.invoice'].create(invoice_vals)
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
                'res_id': inv.id,
                'target': 'self',
            }

    @api.multi
    def create_out_shipment(self):
        for claim in self:
            if claim.replace_delivery_picking_id:
                raise except_orm('Delivery Order is Already created for this claim',
                                 'Delivery Order is ' + claim.replace_delivery_picking_id.name)
            pick_type_id = claim.return_picking_id.picking_type_id.return_picking_type_id and claim.return_picking_id.picking_type_id.return_picking_type_id.id or claim.return_picking_id.picking_type_id.id
            new_picking = claim.return_picking_id.copy({
                'move_lines': [],
                'picking_type_id': pick_type_id,
                'state': 'draft',
                'origin': claim.return_picking_id.name + ' - ' + claim.name,
                'claim_id': claim.id
            })
            claim.replace_delivery_picking_id = new_picking.id
            for move in claim.return_picking_id.move_lines:
                move.copy({
                    'product_uom_qty': move.product_uom_qty,
                    'picking_id': new_picking.id,
                    'state': 'draft',
                    'location_id': claim.saleorder_id.picking_ids[0].location_id.id,
                    'location_dest_id': move.location_id.id,
                    'picking_type_id': pick_type_id,
                    'warehouse_id': claim.saleorder_id.warehouse_id.id,
                    'origin_returned_move_id': move.id,
                    'procure_method': 'make_to_stock',
                })
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window',
                'res_id': new_picking.id,
                'context': self._context,
                'target': 'new',
                'flags': {'action_buttons': True}
            }


class ProductSaleClaimLine(models.Model):
    _name = 'sale.claim.line'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    uom_id = fields.Many2one('product.uom', string='UOM', readonly=True)
    claim_id = fields.Many2one('sale.claim', string='Claim')
    ordered_qty = fields.Float('Ordered Quantity', readonly=True)
    return_qty = fields.Float('Return Quantity')
    claim_desc = fields.Text('Note')
