# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    commission_sale = fields.Many2one('hr.sales.commission', string='Comision a elegir')
    commission = fields.Float('Comision')
    #state_id = fields.Many2one('res.country.state', 'Estado', related="partner_id.state_id", store=True)

    # manager_id = fields.Many2one('res.users', 'Gerente')
    # currency_id_bs = fields.Many2one('res.currency', 'currency', compute='_compute_currency_bs')


    # @api.depends()       
    def _compute_currency_bs(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',3)])
        self.currency_id_bs = currency.id

    @api.onchange('commission_sale')
    def _calc_commission_sale(self):
        for record in self:
                if record.commission_sale.rules_type == 'percent':
                    record.commission = record.amount_untaxed * record.commission_sale.amount_commission / 100
                if record.commission_sale.rules_type == 'fixed':
                    record.commission = record.commission_sale.amount_commission
            
                else:
                    record.commission = 0.0
           
                
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'commission': self.commission,
            'invoice_user_id': self.user_id.id,
            'commission_sale': self.commission_sale.id,
            # 'manager_id': self.manager_id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids.filtered(lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals
        
