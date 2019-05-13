# -*- encoding: utf-8 -*-
from odoo import fields, api, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class WizardStockInternalTransfer(models.TransientModel):
    _inherit = 'wizard.stock.internal.transfer'

    @api.model
    def default_get(self, fields):
        if self._context is None: self._context = {}
        res = models.TransientModel.default_get(self, fields)
        transfer_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')

        if not transfer_ids or len(transfer_ids) != 1:
            return res

        assert active_model in ('stock.internal.transfer'), 'Bad context propagation'
        transfer_id, = transfer_ids
        transfers = self.env['stock.internal.transfer'].browse(transfer_id)

        company_id = self.env['res.users'].browse(self._uid).company_id.id
        company = self.env['res.company'].browse(company_id)

        items = []

        if not company.transit_location_id:
            raise UserError(_("Please setup your stock transit location in Setting - Internal Transfer Configuration"))

        if transfers.state == 'waiting':
            source_location_id = transfers.source_warehouse_id.lot_stock_id.id
            dest_location_id = company.transit_location_id.id
        elif transfers.state == 'send':
            source_location_id = company.transit_location_id.id
            dest_location_id = transfers.dest_warehouse_id.lot_stock_id.id

        for transfer in transfers.line_ids:
            item = {
                'product_id': transfer.product_id.id,
                'product_uom_id': transfer.product_uom_id.id,
                'product_qty': transfer.product_qty,
                'source_location_id': source_location_id,
                'dest_location_id': dest_location_id
            }
            if transfer.product_id:
                items.append(item)

        res.update(item_ids=items)
        return res

    @api.multi
    def button_confirm(self):
        for tf in self:
            if 'active_ids' in self._context:
                transfer = self.env['stock.internal.transfer'].browse(self._context.get('active_ids')[0])
                company = self.env['res.users'].browse(self._uid).company_id
                user_list = transfer.source_warehouse_id.user_ids._ids

                if transfer.state == 'waiting':
                    backorders = []

                    if self._uid not in user_list:
                        raise UserError(_('You are not authorized to send or receive products !'))

                    for line in tf.item_ids:
                        for trans in transfer.line_ids:
                            if line.product_id.id == trans.product_id.id:
                                if line.product_qty > trans.product_qty:
                                    raise UserError(_('You have exceed the available product quantity.'))
                                elif line.product_qty < trans.product_qty:
                                    backorder = {
                                        'product_id': line.product_id.id,
                                        'product_qty': trans.product_qty - line.product_qty,
                                        'product_uom_id': line.product_uom_id.id,
                                        'state': 'draft',
                                    }
                                    backorders.append(backorder)

                    if backorders:
                        create_id = self.env['stock.internal.transfer'].create({
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'source_location_id': transfer.source_location_id.id,
                            'dest_location_id': transfer.dest_location_id.id,
                            'backorder_id': self._context.get('active_ids')[0],
                            'state': 'waiting',
                        })
                        for backorder in backorders:
                            backorder['transfer_id'] = create_id.id
                            self.env['stock.internal.transfer.line'].create(backorder)

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
                                    })

                    transfer.action_send()

                elif transfer.state == 'send':
                    backorders = []

                    if self._uid not in user_list:
                        raise UserError(_('You are not authorized to send or receive product !'))

                    for line in tf.item_ids:
                        for trans in transfer.line_ids:
                            if line.product_id.id == trans.product_id.id:
                                if line.product_qty > trans.product_qty:
                                    raise UserError(_('You have exceed the available product quantity'))
                                elif line.product_qty < trans.product_qty:
                                    backorder = {
                                        'product_id': line.product_id.id,
                                        'product_qty': trans.product_qty - line.product_qty,
                                        'product_uom_id': line.product_uom_id.id,
                                        'state': 'draft',
                                    }
                                    backorders.append(backorder)

                    if backorders:
                        create_id = self.env['stock.internal.transfer'].create({
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'source_location_id': transfer.source_location_id.id,
                            'dest_location_id': transfer.dest_location_id.id,
                            'backorder_id': self._context.get('active_ids')[0],
                            'state': 'send',
                        })
                        for backorder in backorders:
                            backorder['transfer_id'] = create_id.id
                            self.env['stock.internal.transfer.line'].create(backorder)

                        picking_types = picking_type_obj.search([('default_location_dest_id', '=', transfer.dest_warehouse_id.lot_stock_id.id),
                            ('code', '=', 'incoming')])

                        if picking_types:
                            for picking_type in picking_types:
                                picking = picking_obj.create({
                                    'picking_type_id' : picking_type.id,
                                    'transfer_id' : transfer.id,
                                    'location_id': company.transit_location_id.id,
                                    'location_dest_id': transfer.dest_warehouse_id.lot_stock_id.id,
                                })

                                for line in transfer.line_ids:
                                    move_obj.create({
                                        'name' : 'Stock Internal Transfer',
                                        'product_id' : line.product_id.id,
                                        'product_uom' : line.product_uom_id.id,
                                        'product_uom_qty' : line.product_qty,
                                        'location_id' : company.transit_location_id.id,
                                        'location_dest_id' : transfer.dest_warehouse_id.lot_stock_id.id,
                                        'picking_id' : picking.id,
                                    })

                    transfer.action_receive()
                        
        return True