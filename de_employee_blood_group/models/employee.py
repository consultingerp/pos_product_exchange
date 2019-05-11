from odoo import models,fields,api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    blood_group = fields.Selection([('O+','O+'),
                                ('O-','O-'),
                                ('A+','A+'),
                                ('A-','A-'),
                                ('B+','B+'),
                                ('B-','B-'),
                                ('AB+','AB+'),
                                ('AB-','AB-'),],'Blood Group')
