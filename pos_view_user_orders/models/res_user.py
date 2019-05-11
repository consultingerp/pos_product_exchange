# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################

from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_pos_order = fields.Boolean(string="Show User's Orders Only")

    @api.model
    def create(self, values):
        group_id =  self.env.ref('pos_view_user_orders.group_show_user_order_only') or False
        if group_id and 'restrict_pos_order' in values:
            group_name = 'in_group_'+str(group_id.id)
            if(values.get('restrict_pos_order')):
                values[group_name] = True
            else:
                values[group_name] = False
        return super(ResUsers, self).create(values)

    
    @api.multi
    def write(self, vals):
        group_id =  self.env.ref('pos_view_user_orders.group_show_user_order_only') or False
        if group_id and 'restrict_pos_order' in vals:
            group_name = 'in_group_'+str(group_id.id)
            if(vals.get('restrict_pos_order')):
                vals[group_name] = True
            else:
                vals[group_name] = False
        return super(ResUsers, self).write(vals)
                
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_restrict_pos_order_view = fields.Boolean("Show login user's POS Orders only", implied_group='pos_view_user_orders.group_show_user_order_only')

    
