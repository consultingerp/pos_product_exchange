# -*- encoding: utf-8 -*-
import time
from odoo import fields, api, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp

class StockInternalTransfer(models.Model):
    _inherit = 'stock.internal.transfer'

    @api.model
    def create(self, vals):
        if 'source_warehouse_id' in vals:
            warehouse = self.env['stock.warehouse'].browse(vals['source_warehouse_id'])
            if warehouse.sequence_id:
                vals['name'] = self.env['ir.sequence'].next_by_code(warehouse.sequence_id.code)

        if 'name' not in vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.internal.transfer')
            
        res = super(StockInternalTransfer, self).create(vals)
        return res

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        if self.picking_ids:
            self.picking_ids.action_cancel()
        return True

    @api.multi
    def action_waiting(self):
        move_obj = self.env['stock.move']
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        company = self.env['res.users'].browse(self._uid).company_id

        if not company.transit_location_id:
            raise UserError(_('Please setup your stock transit location in Setting - Internal Transfer Configuration'))

        for transfer in self:
            if not transfer.line_ids:
                raise UserError(_('You cannot confirm a stock transfer which has no line'))

            picking_types = picking_type_obj.search([('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
                ('code', '=', 'outgoing')])

            if picking_types:
                for picking_type in picking_types:
                    picking = picking_obj.create({
                        'picking_type_id' : picking_type.id,
                        'transfer_id' : transfer.id,
                        'location_id': transfer.source_warehouse_id.lot_stock_id.id,
                        'location_dest_id': company.transit_location_id.id,
                    })

                    for line in transfer.line_ids:
                        move_obj.create({
                            'name' : 'Stock Internal Transfer',
                            'product_id' : line.product_id.id,
                            'product_uom' : line.product_uom_id.id,
                            'product_uom_qty' : line.product_qty,
                            'location_id' : transfer.source_warehouse_id.lot_stock_id.id,
                            'location_dest_id' : company.transit_location_id.id,
                            'picking_id' : picking.id,
                            'transfer_line_id': line.id
                        })

                    picking.action_assign()
            else:
                raise UserError(_('Unable to find source location in Stock Picking'))

            transfer.write({
                'state': 'waiting'
            })

        return True

    @api.multi
    def action_send(self):
        move_obj = self.env['stock.move']
        picking = False
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        company = self.env['res.users'].browse(self._uid).company_id

        if not company.transit_location_id:
            raise UserError(_('Please setup your stock transit location in Setting - Internal Transfer Configuration'))

        for transfer in self:
            picking_types = picking_type_obj.search([('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
                ('code', '=', 'outgoing')])

            for picking_type in picking_types:
                picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id)], limit=1)

            if not picking:
                raise UserError(_('Related picking not found! Please recheck your data.'))

            picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                ('code', '=', 'incoming')])
            for picking_type in picking_types:
                new_picking = picking_obj.create({
                    'picking_type_id': picking_type.id,
                    'transfer_id': transfer.id,
                    'location_id': company.transit_location_id.id,
                    'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id,
                })

            for line in transfer.line_ids:
                move_obj.create({
                    'name': 'Stock Internal Transfer',
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'product_uom_qty': line.product_qty,
                    'location_id': transfer.dest_warehouse_id.lot_stock_id.id,
                    'location_dest_id': company.transit_location_id.id,
                    'picking_id': new_picking.id,
                    'transfer_line_id': line.id
                })
                move = move_obj.search([('transfer_line_id', '=', line.id), ('picking_id', '=', picking.id)], limit=1)
                if move and line.out_quantity_done:
                    move.write({
                        'quantity_done': line.out_quantity_done    
                    })

            picking.action_confirm()
            picking.action_assign()
            picking.button_validate()
            immd_trf = self.env['stock.immediate.transfer'].search([('pick_ids', '=', picking.id)])
            immd_trf.process()
            picking.action_done()

            backorder_pick = picking_obj.search([('backorder_id', '=', picking.id)])
            if backorder_pick:
                backorder_pick.action_cancel()
                picking.message_post(body=_("Back order <em>%s</em> <b>cancelled</b>.") % (backorder_pick.name))

            new_picking.action_assign()
            transfer.write({'state': 'send', 'sent_date': time.strftime('%Y-%m-%d %H:%M:%S')})

        return True

    @api.multi
    def action_create_incoming(self):
        picking = False
        move_obj = self.env['stock.move']
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        company = self.env['res.users'].browse(self._uid).company_id

        if not company.transit_location_id:
            raise UserError(_('Please setup your stock transit location in Setting - Internal Transfer Configuration'))

        for transfer in self:
            picking_types = picking_type_obj.search([('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
                ('code', '=', 'outgoing')])

            for picking_type in picking_types:
                picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id)], limit=1)
                
            picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                ('code', '=', 'incoming')])
            for picking_type in picking_types:
                new_picking = picking_obj.create({
                    'picking_type_id': picking_type.id,
                    'transfer_id': transfer.id,
                    'location_id': company.transit_location_id.id,
                    'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id,
                })

            if picking:
                for move in picking.move_lines:
                    move_obj.create({
                        'name': 'Stock Internal Transfer',
                        'product_id': move.product_id.id,
                        'product_uom': move.product_uom.id,
                        'product_uom_qty': move.product_qty,
                        'location_id': company.transit_location_id.id,
                        'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id,
                        'picking_id': new_picking.id,
                    })
            else:
                for line in transfer.line_ids:
                    move_obj.create({
                        'name': 'Stock Internal Transfer',
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom_id.id,
                        'product_uom_qty': line.product_qty,
                        'location_id': company.transit_location_id.id,
                        'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id,
                        'picking_id': new_picking.id,
                        'transfer_line_id': line.id
                    })

            new_picking.action_assign()
            transfer.write({'state': 'send', 'sent_date': time.strftime('%Y-%m-%d %H:%M:%S')})

        return True

    @api.multi
    def action_receive(self):
        picking = False
        move_obj = self.env['stock.move']
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']

        for transfer in self:
            picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                ('code', '=', 'incoming')])

            for picking_type in picking_types:
                picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id)], limit=1)
                
            if not picking:
                raise UserError(_('Related picking not found! Please recheck your data.'))
        
            for line in transfer.line_ids:
                move = move_obj.search([('transfer_line_id', '=', line.id), ('picking_id', '=', picking.id)], limit=1)
                if move and line.in_quantity_done:
                    move.write({
                        'quantity_done': line.in_quantity_done    
                    })

            picking.action_confirm()
            picking.action_assign()
            picking.button_validate()
            immd_trf = self.env['stock.immediate.transfer'].search([('pick_ids', '=', picking.id)])
            immd_trf.process()
            picking.action_done()

            backorder_pick = picking_obj.search([('backorder_id', '=', picking.id)])
            if backorder_pick:
                backorder_pick.action_cancel()
                picking.message_post(body=_("Back order <em>%s</em> <b>cancelled</b>.") % (backorder_pick.name))

            transfer.write({'state': 'done', 'received_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        
        return True

    @api.multi
    def action_print_outgoing(self):
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        context = self._context.copy()

        for transfer in self:
            context['internal_transfer'] = transfer.name

            user_ids = transfer.source_warehouse_id.user_ids
            if self._uid not in user_ids._ids:
                raise UserError(_('You are not authorized to print this picking!'))

            picking_types = picking_type_obj.search([('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
                ('code', '=', 'outgoing')])

            for picking_type in picking_types:
                picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id), ('state', '!=', 'cancel')], limit=1)

                if picking:
                    return picking.with_context(context).do_print_picking()
                else:
                    raise UserError(_('Outgoing not found, please recheck your data!'))

        return True

    @api.multi
    def action_print_incoming(self):
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        context = self._context.copy()

        for transfer in self:
            context['internal_transfer'] = transfer.name

            user_ids = transfer.dest_warehouse_id.user_ids
            if self._uid not in user_ids._ids:
                raise UserError(_('You are not authorized to print this picking!'))

            picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                ('code', '=', 'incoming')])

            for picking_type in picking_types:
                picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id), ('state', '!=', 'cancel')], limit=1)
                if picking:
                    return picking.with_context(context).do_print_picking()
                else:
                    raise UserError(_('Incoming not found, please recheck your data!'))

        return True

    @api.multi
    def action_assign(self):
        move_obj = self.env['stock.move']
        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type']
        company = self.env['res.users'].browse(self._uid).company_id

        for transfer in self:
            if transfer.state == 'waiting':
                picking_types = picking_type_obj.search([('default_location_src_id', '=', transfer.source_warehouse_id.lot_stock_id.id),
                    ('code', '=', 'outgoing')])

                for picking_type in picking_types:
                    picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id)], limit=1)
                    
                    if picking:
                        picking.action_assign()
            elif transfer.state == 'send':
                picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                    ('code', '=', 'incoming')])

                for picking_type in picking_types:
                    picking = picking_obj.search([('transfer_id', '=', transfer.id), ('picking_type_id', '=', picking_type.id)], limit=1)
                    
                    if picking:
                        picking.action_assign()

        return True

    name = fields.Char(string= 'Reference', track_visibility="onchange", default=None)
    state = fields.Selection([('cancel', 'Cancel'), ('draft', 'Draft'), ('waiting', 'Waiting'), ('send', 'Send'), ('done', 'Done')], string="Status", track_visibility="onchange", default="draft")
    line_ids = fields.One2many('stock.internal.transfer.line', 'transfer_id', string="Stock Internal Transfer Line", copy=True)
    sent_date = fields.Datetime('Sent Date')
    received_date = fields.Datetime('Received Date')

class StockInternalTransferLine(models.Model):
    _inherit = 'stock.internal.transfer.line'

    def unlink(self):
        if any(line.transfer_id.state not in ('draft') for line in self):
            raise UserError(_('You can only delete draft moves.'))
        return super(StockInternalTransferLine, self).unlink()

    @api.multi
    @api.depends('move_ids.move_line_ids.product_qty')
    def _compute_reserved_availability(self):
        move_obj = self.env['stock.move']
        reserved_availability = 0

        for line in self:
            for picking in line.transfer_id.picking_ids:
                if picking.picking_type_id.warehouse_id.id == line.transfer_id.source_warehouse_id.id:
                    move = move_obj.search([('transfer_line_id', '=', line.id), ('location_id', '=', line.transfer_id.source_warehouse_id.lot_stock_id.id), ('state', 'not in', ['cancel', 'done'])])
                    if move:
                        result = {data['move_id'][0]: data['product_qty'] for data in 
                            self.env['stock.move.line'].read_group([('move_id', '=', move.id), ('picking_id', '=', picking.id)], ['move_id','product_qty'], ['move_id'])}
                        reserved_availability = move.product_id.uom_id._compute_quantity(result.get(move.id, 0.0), move.product_uom, rounding_method='HALF-UP')

            line.reserved_availability = reserved_availability

    reserved_availability = fields.Float('Reserved', compute='_compute_reserved_availability', digits=dp.get_precision('Product Unit of Measure'))
    out_quantity_done = fields.Float('Done (Out)')
    in_quantity_done = fields.Float('Done (In)')
    move_ids = fields.One2many('stock.move', 'transfer_line_id', string="Stock Moves", track_visibility="onchange")