from odoo import fields, models, api
from datetime import datetime, date

class CrmSaleTeam(models.Model):
    _inherit = 'crm.lead'
    
    expected_income_dollars = fields.Monetary(string='Ingreso esperado en dolares', currency_field='currency_id_usd')
    currency_id_usd = fields.Many2one('res.currency', 'currency', compute='_compute_currency_dollars')

    @api.depends()       
    def _compute_currency_dollars(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        self.currency_id_usd = currency.id

    @api.onchange('expected_income_dollars')
    def onchange_conversion_expected_income_bs(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        for record in self:
            if currency:
                for c in currency:
                    record.expected_revenue = record.expected_income_dollars * c.res_currency

    @api.onchange('expected_revenue')
    def onchange_conversion_expected_income_dollar(self):
        valor=0
        for record in self:
            currency = self.env['res.currency.rate'].search([('currency_id','=',2)],order='name asc')
            if currency:
                for tasa in currency:
                    valor=record.expected_revenue / tasa.inverse_company_rate
            record.expected_income_dollars=valor