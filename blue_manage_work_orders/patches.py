# -*- coding: utf-8 -*-
from odoo import api, models, fields

# =============================================================================
# This file is exclusively for monkey patches.  Please do not put any patches
# in to your model directory source files.  This is basically a way to collect
# all of the module's patches in to one place so if there are any side effects
# or bugs that are happening because of a patch, it'll be easier to debug.
#
# In general you will want to format this so that there's an explaination,
# import, method definition (with further explaination in it's doc string),
# then patch assignment.  An Example:
#
#   # Monkey patch to stop interference with Odoo's default way of setting
#   # planning dates.
#   from openerp.addons.mrp_operations.mrp_operations import mrp_production
#
#   @api.multi
#   def new_write(self, vals):
#       """
#       Monkey patch the `write` method to ensure that ... explaination ...
#
#       :param vals: A Dictionary
#       :return: True (as per super)
#       """
#       # New patch code goes here
#       return super(mrp_production, self).write(vals)
#
#   mrp_production.write = new_write
#
# =============================================================================
