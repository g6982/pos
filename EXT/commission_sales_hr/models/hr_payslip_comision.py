# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import pandas as pd
from odoo.exceptions import UserError, ValidationError

class HrPayslipComision(models.Model):
    _name = 'hr.payslip.comision'

    payslip_id = fields.Many2one('hr.payslip')
    factura_id = fields.Many2one('account.move')
    monto_fact = fields.Monetary()
    monto_base = fields.Monetary()
    currency_id = fields.Many2one('res.currency')
    monto_commission = fields.Monetary()
    monto_commission_bs = fields.Float()
    fecha_fact = fields.Date()
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company.id)
    commission_sale = fields.Many2one('hr.sales.commission')

#registro de comision en nomina