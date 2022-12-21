# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    commission = fields.Float('Comision')
    commission1 = fields.Float('Comision Usd')
    commission_sale = fields.Many2one('hr.sales.commission', string='Comision a elegir')
    state_id = fields.Many2one('res.country.state', 'Estado', related="partner_id.state_id", store=True)

    # manager_id = fields.Many2one('res.users', 'Gerente')

    
