# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import timedelta, date, datetime
from odoo.exceptions import UserError

class Templatesaleorder(models.Model):
    _inherit = "sale.order"

#    calculation = fields.Char(readonly=True)
 #   cant_r = fields.Float('Factor', store=True)
  #  cant_p = fields.Char('Porcentaje', store=True)
  #  segmentos_id = fields.Many2one('stock.segmentos')

   # @api.onchange('cost_usd')
   # def margen_ganancia(self):
    #    for record in self:
     #       if record.calculation == "Factor de utilidad":
      #          precio_dolar = record.cost_usd
       #         revenue = precio_dolar * 1 / float(self.cant_r)
        #        record.list_price = revenue

         #   if record.calculation == "Porcentaje de ganancia":
          #      precio_dolar = record.cost_usd
           #     porcentaje = precio_dolar * float(record.cant_p) / 100
            #    record.list_price = record.cost_usd + porcentaje   
