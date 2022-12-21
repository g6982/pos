# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class HrSalesGoal(models.TransientModel):
    _name = 'hr.sales.goal'
    _order = 'id desc'

    user_ids = fields.Many2many('res.users', string='Vendedores')
    date_start = fields.Date(string='Desde')
    date_stop = fields.Date(string="Hasta")
    commission_invoice_ids = fields.Many2many(comodel_name='hr.commission.invoice', string='Comisiones')
   

    def float_format(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result = "0,00"
        return result

    def print_report_sale(self):
        for user in self.user_ids:

            invoice=self.env['account.move'].search([('invoice_user_id','=',user_id.id),('payment_state','in',('paid','paid')),('invoice_date','>=',self.date_start),('invoice_date','<=',self.date_stop)])
           # invoice=self.env['account.move'].search([('invoice_user_id','=',user.id),('invoice_date','>=',self.date_start),('invoice_date','<=',self.date_stop)])
            if invoice:
                for det in invoice:
                    value=({
                        'account_id':det.id,
                        })
                    self.env['hr.commission.invoice'].create(value)
            self.commission_invoice_ids=self.env['hr.commission.invoice'].search([])
                #raise UserError(_('invoice= %s')%invoice)
            #[data] = self.read()
            #sale_list = []
        #return self.env.ref('commission_sales_hr.action_report_sale').report_action(invoice, data=data)
        return {'type': 'ir.actions.report','report_name': 'commission_sales_hr.sale_report_quimica','report_type':"qweb-pdf"}


class HrCommissionInvoice(models.Model):
    _name = 'hr.commission.invoice'
    _order = 'id desc'

    account_id = fields.Many2one('account.move')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company.id)


    def float_format(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result = "0,00"
        return result


class HrSalesGoalQuaterly(models.Model):
    _name = 'hr.sales.goal.quaterly'
    _order = 'id desc'

    rules_type = fields.Selection([
        ('fixed', 'Monto Fijo'),
        ('percent', 'Porcentaje'),
    ], 'Tipo de Comisión', default='fixed')
    name = fields.Char(string='Nombre de la meta')
    user_ids = fields.Many2many('res.users', string='Vendedores o Gerentes')
    amount_goal = fields.Float(string='Meta de ventas trimestral')
    # tax_period = fields.Char('Periodo Tributario', required=True, default=lambda *a: datetime.now().strftime('%Y-%m'))
    percentage_goal = fields.Float(string='Porcentaje de la meta a cumplir') 
    percentage_goal_top = fields.Float(string='Porcentaje maximo de la meta') 
    amount_commission = fields.Float(string='Monto comision')
    amount_commission_usd = fields.Float(string='Monto comision usd')
    type_goal = fields.Selection([('pool', 'Pool'), ('region', 'Region')], string="Tipo de meta")
    type_entry = fields.Many2one('hr.payslip.input.type', 'Tipo de entrada')
   


    
        
    @api.onchange('amount_commission_usd')
    def onchange_conversion_amount_commission_bs(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        for record in self:
            if currency:
                if record.rules_type == 'fixed':
                    for c in currency:
                        record.amount_commission = record.amount_commission_usd * c.res_currency
                if record.rules_type == 'percent':
                    record.amount_commission_usd = ''

    @api.onchange('amount_commission')
    def onchange_conversion_amount_commission_dollar(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        for record in self:
            if currency:
                if record.rules_type == 'fixed':
                    for c in currency:
                        record.amount_commission_usd = record.amount_commission / c.res_currency
                if record.rules_type == 'percent':
                    record.amount_commission_usd = ''
    # tax_period_quaterly = fields.Char('Periodo Trimestrales')
    
    # @api.onchange('tax_period')
    # def calc_tax_period_quaterly(self):
    #     if self.tax_period:
    #         current = datetime.strptime(self.tax_period + '-01', '%Y-%m-%d')
    #         periods = ''
    #         first_quaterly = current + relativedelta(months=2)
    #         periods += first_quaterly.strftime('%Y-%m') + ','
            
    #         second_quaterly = current + relativedelta(months=6)
    #         periods += second_quaterly.strftime('%Y-%m') + ','
            
    #         third_quaterly = current + relativedelta(months=9)
    #         periods += third_quaterly.strftime('%Y-%m') + ','
    

    #         last_quaterly = current + relativedelta(months=12)
    #         periods += last_quaterly.strftime('%Y-%m')
            
    #         self.tax_period_quaterly = periods


class HrSalesCommission(models.Model):
    _name = 'hr.sales.commission'
    _order = 'id desc'

    name = fields.Char(string='Nombre de la comision')
    user_ids = fields.Many2many('res.users', string='Vendedores ')
    rules_type = fields.Selection([
        ('fixed', 'Monto Fijo'),
        ('percent', 'Porcentaje'),
    ], 'Tipo de Comisión', default='fixed')
    amount_commission = fields.Float(string='Monto o porcentaje de comision')
    amount_commission_usd = fields.Float(string='Monto comision usd')
  
    

    @api.onchange('amount_commission_usd')
    def onchange_conversion_amount_commission_bs(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        for record in self:
            if currency:
                if record.rules_type == 'fixed':
                    for c in currency:
                        record.amount_commission = record.amount_commission_usd * c.res_currency
                if record.rules_type == 'percent':
                    record.amount_commission_usd = ''

    @api.onchange('amount_commission')
    def onchange_conversion_amount_commission_dollar(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        for record in self:
            if currency:
                if record.rules_type == 'fixed':
                    for c in currency:
                        record.amount_commission_usd = record.amount_commission / c.res_currency
                if record.rules_type == 'percent':
                    record.amount_commission_usd = ''








"""def print_report_sale(self):
            sale = self.env['sale.order'].search([('date_order', '>=', self.date_start), ('date_order', '<=', self.date_stop)])
            [data] = self.read()
            sale_list = []

            if sale:
                if self.product_ids:
                    for s in sale:
                        for sl in s.order_line.filtered(lambda sl: sl.product_id.id in self.product_ids.ids):
                                sale_dict = {'date_order': s.date_order,
                                        'partner_id': s.partner_id.name,
                                        'repre_sale': s.user_id.name,
                                        'city': s.partner_id.city or '',
                                        'country_id': s.partner_id.country_id.name or '',
                                        'state_id': s.partner_id.state_id.name or '',
                                        'product_id': sl.product_id.name,
                                        'product_qty': sl.product_uom_qty,
                                        'amount':  sl.price_unit,
                                        'currency_id': s.currency_id.name,
                                        'amount_total': sl.price_unit * sl.product_uom_qty,
                                            }
                                sale_list.append(sale_dict)
                    data['sale'] = sale_list

                if not self.product_ids:
                    for s in sale:
                        for sl in s.order_line:
                                sale_dict = {'date_order': s.date_order,
                                        'partner_id': s.partner_id.name,
                                        'repre_sale': s.user_id.name,
                                        'city': s.partner_id.city or '',
                                        'country_id': s.partner_id.country_id.name or '',
                                        'state_id': s.partner_id.state_id.name or '',
                                        'product_id': sl.product_id.name,
                                        'product_qty': sl.product_uom_qty,
                                        'amount':  sl.price_unit,
                                        'currency_id': s.currency_id.name,
                                        'amount_total': sl.price_unit * sl.product_uom_qty,
                                            }
                                sale_list.append(sale_dict)
                    data['sale'] = sale_list
                    
            if not self.date_start and not self.date_stop and self.product_ids:
                sale = self.env['sale.order'].search([])
                [data] = self.read()
                sale_list = []
                for s in sale:
                    for sl in s.order_line.filtered(lambda sl: sl.product_id.id in self.product_ids.ids):
                            sale_dict = {'date_order': s.date_order,
                                        'partner_id': s.partner_id.name,
                                        'repre_sale': s.user_id.name,
                                        'city': s.partner_id.city or '',
                                        'country_id': s.partner_id.country_id.name or '',
                                        'state_id': s.partner_id.state_id.name or '',
                                        'product_id': sl.product_id.name,
                                        'product_qty': sl.product_uom_qty,
                                        'amount':  sl.price_unit,
                                        'currency_id': s.currency_id.name,
                                        'amount_total': sl.price_unit * sl.product_uom_qty,
                                        }
                            sale_list.append(sale_dict)
                data['sale'] = sale_list
            
                
            if not self.date_start and not self.date_stop and not self.product_ids:
                sale = self.env['sale.order'].search([])
                [data] = self.read()
                sale_list = []
                for s in sale:
                    for sl in s.order_line:
                            sale_dict = {'date_order': s.date_order,
                                        'partner_id': s.partner_id.name,
                                        'repre_sale': s.user_id.name,
                                        'city': s.partner_id.city or '',
                                        'country_id': s.partner_id.country_id.name or '',
                                        'state_id': s.partner_id.state_id.name or '',
                                        'product_id': sl.product_id.name,
                                        'product_qty': sl.product_uom_qty,
                                        'amount':  sl.price_unit,
                                        'currency_id': s.currency_id.name,
                                        'amount_total': sl.price_unit * sl.product_uom_qty,
                                        }
                            sale_list.append(sale_dict)
                data['sale'] = sale_list

            return self.env.ref('commission_sales_hr.action_report_sale').report_action(sale, data=data)"""