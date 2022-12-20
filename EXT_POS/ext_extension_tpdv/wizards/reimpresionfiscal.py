from datetime import datetime, timedelta
from email.policy import default
from xml.dom.minidom import Document
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import logging

import io
from io import BytesIO

import xlsxwriter
import shutil
import base64
import csv
import xlwt

_logger = logging.getLogger(__name__)

class ReimpresionFiscal(models.TransientModel):
   
    _name = "reimpresion.fiscal" 

    name = fields.Selection([('date', 'Rango de Fecha'),('document',' Rango de Documento')], string='Modo de Reimpresion',default="date")
    document = fields.Selection([
        ('f', 'Factura'),
        ('c', 'Nota de Credito'),
        ('d', 'Nota de Debito'),
        ('x', 'Reporte X'),
        ('z', 'Reporte Z'),
    ], string='Documento',default="f")
    
    date_init = fields.Date('Desde')
    date_end  = fields.Date('Hasta')

    number_init = fields.Integer('Desde')
    number_end  = fields.Integer('Hasta')

    def fecha_formato(self,fecha):
        y = str(fecha.year)
        valor =    '0'  + '{:>2}'.format(y[2:4])
        valor +=   '{:>2}'.format( str(fecha.month)) 
        valor +=   '{:>2}'.format(str(fecha.day)) 
        return valor.replace(' ','0')

    @api.onchange('date_init', 'date_end')
    def onchange_fecha(self):
        if self.date_end and self.date_init:
            if self.date_end < self.date_init:
                raise UserError(_(' La Fecha Hasta No debe de ser mayor a la Fecha de Inicio'))
    
    @api.onchange('number_init', 'number_end')
    def onchange_numero(self):
        if self.number_end and self.number_init:
            if self.number_end < self.number_init:
                raise UserError(
                    _(' La Numero Hasta No debe de ser mayor al Numero de Inicio'))


    @api.onchange('name')
    def onchange_name(self):
        self.date_init = False
        self.date_end = False
        self.number_init = False
        self.number_end = False
    
    def imprimir(self):
        valor_url = "http://localhost/fiscal_13/reimpresion.php?reimprimir="
        if self.name == 'date':
            valor_url += "R" + self.document
            valor_url += self.fecha_formato(self.date_init)
            valor_url += self.fecha_formato(self.date_end)
        else :
            valor_url += "R" + self.document.upper()
            valor_url += '{:>7}'.format(str(self.number_init))
            valor_url += '{:>7}'.format(str(self.number_end))
            valor_url = valor_url.replace(' ','0')
        return {
            'type': 'ir.actions.act_url',
            'name': "Reimpresion",
            'target': 'self',
            'url': valor_url,
        }
