# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import pandas as pd
from odoo.exceptions import UserError, ValidationError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    commission_line_ids = fields.One2many('hr.payslip.comision', 'payslip_id', string='Pagos')
    monto_resumen_commission = fields.Float(compute='_compute_suma_comision')

    @api.onchange('commission_line_ids.monto_commission_bs','struct_id')
    def _compute_suma_comision(self):
        for selff in self:
            total=0
            for det in selff.commission_line_ids:
                total=total+det.monto_commission_bs
            selff.monto_resumen_commission=total
    
    def calc_commission(self,total_invoices,goal):
        """
            Method that calculates the commission of the employee who met the sales goal
            @total_invoices(recordset): sales or invoiced
            @goal(recordset): goal recordset
        """
        if goal.rules_type == 'fixed':
           return goal.amount_commission
        else:
            commission = total_invoices * goal.amount_commission / 100
            return commission
    
    """Comisiones`por venta de empleados en nomina   """
    
    def get_commission_employee(self):
        """
            Method that brings the commission of the employee
            @config: settings
            return commission
        """
        period_dates = pd.date_range(start=self.date_from, end=self.date_to)
        dates = [date for date in period_dates.date]
        invoices = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('user_id', '=', self.employee_id.user_id.id),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        invoices_pool = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        invoices_region = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('state_id', '=', self.employee_id.address_id.state_id.id),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])

        #invoices = self.env['account.move'].search([('state', 'in', ['posted']), ('move_type', '=', 'out_invoice'), ('user_id', '=', self.employee_id.user_id.id), ('invoice_date', '<=', self.date_to),('invoice_date', '>=', self.date_from)])
        total_inv = sum(inv.amount_untaxed_signed for inv in invoices) if invoices else 0
        total_inv_pool = sum(inv.amount_untaxed_signed for inv in invoices_pool) if invoices else 0
        total_inv_region = sum(inv.amount_untaxed_signed for inv in invoices_region) if invoices else 0

        goal_emp = self.env['hr.sales.goal'].search([])
        if goal_emp:
            goal_emp_filt = goal_emp.filtered(lambda g: self.employee_id.user_id.id in g.user_ids.ids)
            # goal_selected = goal_emp_filt[0] if goal_emp_filt else False
            sale_goal = 0
            comission = 0
            comissions_list = []
            for goal_selected in goal_emp_filt:
                if goal_selected.type_goal == 'pool':
                    total_inv = total_inv_pool
                if goal_selected.type_goal == 'region':
                    total_inv = total_inv_region
                sale_goal = goal_selected.amount_goal
                if goal_selected.percentage_goal > 0.0:
                    sale_goal = sale_goal * goal_selected.percentage_goal / 100
                if total_inv >= sale_goal:
                    comission = self.calc_commission(total_inv, goal_selected)
                    if comission > 0:
                        comissions_list.append({
                            'input_type_id': goal_selected.type_entry.id,
                            'amount': comission
                        })
            return comissions_list
        else:
            return False
        
   
   
    def get_commission_sale_employee(self):
        """
            Method that brings the commission sale of the employee
            @config: settings
            return commission
        """
        period_dates = pd.date_range(start=self.date_from, end=self.date_to)
        dates = [date for date in period_dates.date]
        invoices = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('user_id', '=', self.employee_id.user_id.id),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        total_inv = sum(inv.commission for inv in invoices) if invoices else 0
        #invoices = self.env['account.move'].search([('state', 'in', ['posted']), ('move_type', '=', 'out_invoice'), ('user_id', '=', self.employee_id.user_id.id), ('invoice_date', '<=', self.date_to),('invoice_date', '>=', self.date_from)])
        # commission_emp_filt = invoices.filtered(lambda c: self.employee_id.user_id.id in c.user_id.id)
        comissions_list=[]
        if invoices.commission_sale:
            comissions_list.append({
                            'input_type_id':  invoices.commission_sale.type_entry.id,
                            'amount': total_inv
                        })
            return comissions_list
        else:
            return False
            
        
        
        
    def get_commission_employee_quaterly(self):
        """
            Method that brings the commission of the employee
            @config: settings
            return commission
        """
        date_init = self.date_from - relativedelta(months=2)
        period_dates = pd.date_range(start=date_init, end=self.date_to)
        dates = [date for date in period_dates.date]
        invoices = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('user_id', '=', self.employee_id.user_id.id),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        invoices_pool = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        invoices_region = self.env['account.move'].search([('state', 'in', ['posted']),('move_type','in',['out_invoice', 'out_refund']),('state_id', '=', self.employee_id.address_id.state_id.id),('invoice_date', 'in', dates), ('payment_state','in', ['paid', 'reversed'])])
        #invoices = self.env['account.move'].search([('state', 'in', ['posted']), ('move_type', '=', 'out_invoice'), ('user_id', '=', self.employee_id.user_id.id), ('invoice_date', '<=', self.date_to),('invoice_date', '>=', self.date_from)])
        total_inv = sum(inv.amount_untaxed_signed for inv in invoices) if invoices else 0
        total_inv_pool = sum(inv.amount_untaxed_signed for inv in invoices_pool) if invoices else 0
        total_inv_region = sum(inv.amount_untaxed_signed for inv in invoices_region) if invoices else 0


        goal_emp = self.env['hr.sales.goal.quaterly'].search([])
        if goal_emp:
            goal_emp_filt = goal_emp.filtered(lambda g: self.employee_id.user_id.id in g.user_ids.ids)
            # goal_selected = goal_emp_filt[0] if goal_emp_filt else False
            sale_goal = 0
            comission = 0
            comissions_list=[]
            # period = self.date_from.strftime('%Y-%m')
            for goal_selected in goal_emp_filt:
                if goal_selected.type_goal == 'pool':
                    total_inv = total_inv_pool
                if goal_selected.type_goal == 'region':
                    total_inv = total_inv_region
                # tax_period_quaterly = goal_selected.tax_period_quaterly.split(",")
                # if period in tax_period_quaterly:
                sale_goal = goal_selected.amount_goal
                if goal_selected.percentage_goal > 0.0:
                    sale_goal = sale_goal * goal_selected.percentage_goal / 100
                if total_inv >= sale_goal:
                    comission = self.calc_commission(total_inv, goal_selected)
                    if comission > 0:
                        comissions_list.append({
                            'input_type_id': goal_selected.type_entry.id,
                            'amount': comission
                        })
            return comissions_list
        else:
            return False
       



    @api.onchange('employee_id','date_from','date_to')
    def _compute_comision(self):
        tipo_comision=self.env['hr.payslip.comision'].search([]).unlink()
        busca=self.env['account.move'].search([('invoice_user_id','=',self.employee_id.user_id.id),('payment_state','in',('in_payment','paid')),('invoice_date','>=',self.date_from),('invoice_date','<=',self.date_to)])
        if busca:
            for item in busca:
                commission=item.commission
                """value={
                    'input_type_id':9,
                    'amount':commission,
                    'payslip_id':self.id,
                    'contract_id':self.struct_id.id,
                }
                self.input_line_ids.create(value)"""
                self.registra_comision(commission,self.id,item)
                #raise UserError(_('commission=%s')%commission)


# metodo para registrar las comisiones en la nomina 

    def registra_comision(self,commission,id_payslip,factura):
        tipo_comision=self.env['hr.payslip.comision']
        value={
            'monto_commission':commission,
            'monto_commission_bs':commission*self.os_currecy_rate_gene if factura.currency_id.id!=self.env.company.currency_id.id else commission,
            'payslip_id':id_payslip,
            'factura_id':factura.id,
            'monto_fact':factura.amount_total,
            'monto_base':factura.amount_untaxed,
            'currency_id':factura.currency_id.id,
            'fecha_fact':factura.invoice_date,
            'commission_sale':factura.commission_sale.id,
            }
        tipo_comision.create(value)
