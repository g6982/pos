# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosConfig(models.Model):
    _inherit = 'pos.order'

    nb_caja_comp=fields.Char(string="Registro de Máquina Fiscal",compute='_compute_nb_caja')
    nb_caja=fields.Char(string="Registro de nombre de la caja")
    status_impresora = fields.Char(default="no")
    tipo = fields.Char(default="venta")
    tasa_dia = fields.Float(compute="_compute_tasa")

    url_nota_credito=fields.Char(string="Imprimir Nota de Credito",readonly="True")
    id_order_afectado=fields.Char()
    link=fields.Char(compute='_compute_link')


    def _compute_tasa(self):
        tasa=0
        for selff in self:
            #lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_order)],order='id ASC')
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=',2 )],order='id desc')
            if lista_tasa[0]:
                for det in lista_tasa[0]:
                    tasa=det.rate
            selff.tasa_dia=tasa


    def _compute_nb_caja(self):
        self.nb_caja_comp=self.session_id.config_id.nb_identificador_caja
        self.nb_caja=self.nb_caja_comp

    """def refund(self):
        super().refund()
        self.nro_fact_seniat=0"""

    #@api.depends('state')
    @api.onchange('state')
    def _compute_link(self):
        valor_url='http://localhost:8080/impresora_fiscal/nota_credito.php'
        for selff in self:
            selff.link=valor_url+'?id_order_afectado='+str(selff.id_order_afectado)+'&order_nc='+str(selff.id)+'&pos_reference='+str(selff.pos_reference) 
            selff.url_nota_credito=selff.link

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    status_impresora=fields.Char(related='order_id.status_impresora')
    tipo = fields.Char(related='order_id.tipo')

class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    def check(self):
        res = super(PosMakePayment, self).check()
        ordenes = self.env['pos.order'].browse(self.env.context.get('active_id', False))
        pos_reference=ordenes.pos_reference
        actualiza=self.env['pos.order'].search([('pos_reference','=',pos_reference),('amount_total','>','0')])
        for det in actualiza:
            id_order_org=det.id
        ordenes.id_order_afectado=id_order_org
        ordenes.tipo="devolucion"

        #raise UserError(_('pos_reference= %s')%ordenes.pos_reference)
