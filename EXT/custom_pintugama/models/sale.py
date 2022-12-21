from email.policy import default
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    indirect_check = fields.Boolean(string="Indirecto")
   # expected_revenue = fields.Integer(string="Ingreso Esperado")
    expected_income_dollars = fields.Integer(string='Ingreso esperado en dolares', currency_field='currency_id_usd')
    state_id = fields.Many2one('res.country.state', 'Estado', related="partner_id.state_id", store=True)
    city = fields.Char('Ciudad', related='partner_id.city', store=True)
    currency_id_usd = fields.Many2one('res.currency.rate.server', 'currency', compute='_compute_currency_dollars')
    asunto = fields.Char(string="Observaciones" )

    #@api.depends()       
    def _compute_currency_dollars(self):
        currency = self.env['res.currency.rate.server'].search([('id','=',2)])
        self.currency_id_usd = currency.id


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

    def fact_div(self,valor):
        self.currency_id.id
        fecha_contable_doc=self.date
        monto_factura=self.amount_total
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.currency_id.id!=self.doc_currency_id.id:
            if self.currency_id!=self.company_id.currency_id.id:
                tasa= self.env['account.move'].search([('id','=',self.id)],order="id asc")
                for det_tasa in tasa:
                    monto_nativo=det_tasa.amount_untaxed_signed
                    monto_extran=det_tasa.amount_untaxed
                    valor_aux=abs(monto_nativo/monto_extran)
                rate=round(valor_aux,3)  # LANTA
                #rate=round(valor_aux,2)  # ODOO SH
                resultado=valor*rate
            else:
                resultado=valor
        else:
            resultado=valor
        return resultado

    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado



    def doc_cedula(self,aux):
        #nro_doc=self.partner_id.vat
        busca_partner = self.env['res.partner'].search([('id','=',aux)])
        for det in busca_partner:
            tipo_doc=busca_partner.doc_type
            if busca_partner.vat:
                nro_doc=str(busca_partner.vat)
            else:
                nro_doc="00000000"
            tipo_doc=busca_partner.doc_type
        nro_doc=nro_doc.replace('V','')
        nro_doc=nro_doc.replace('v','')
        nro_doc=nro_doc.replace('E','')
        nro_doc=nro_doc.replace('e','')
        nro_doc=nro_doc.replace('G','')
        nro_doc=nro_doc.replace('g','')
        nro_doc=nro_doc.replace('J','')
        nro_doc=nro_doc.replace('j','')
        nro_doc=nro_doc.replace('P','')
        nro_doc=nro_doc.replace('p','')
        nro_doc=nro_doc.replace('-','')
        
        if tipo_doc=="v":
            tipo_doc="V"
        if tipo_doc=="e":
            tipo_doc="E"
        if tipo_doc=="g":
            tipo_doc="G"
        if tipo_doc=="j":
            tipo_doc="J"
        if tipo_doc=="p":
            tipo_doc="P"
        resultado=str(tipo_doc)+"-"+str(nro_doc)
        return resultado



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    readonly_fields_discount = fields.Boolean('bool')

    # @api.depends('product_id')
    # def _compute_readonly_discount(self):
    #     self.compute_bool = False
    #     for line in self:
    #         if line.order_id.user_id:
    #             if line.order_id.user_id.id == self.env.user.id:
    #                 line.compute_bool = True
    #             if line.compute_bool == True:
    #                     line.readonly_fields_discount = True
    

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
            

        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
            if line.order_id.user_id:
                if line.order_id.user_id.id == self.env.user.id:
                        line.readonly_fields_discount = True
    
    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado

    
    def fact_div(self,valor):
        self.currency_id.id
        fecha_contable_doc=self.date
        monto_factura=self.amount_total
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.currency_id.id!=self.doc_currency_id.id:
            if self.currency_id!=self.company_id.currency_id.id:
                tasa= self.env['account.move'].search([('id','=',self.id)],order="id asc")
                for det_tasa in tasa:
                    monto_nativo=det_tasa.amount_untaxed_signed
                    monto_extran=det_tasa.amount_untaxed
                    valor_aux=abs(monto_nativo/monto_extran)
                rate=round(valor_aux,3)  # LANTA
                #rate=round(valor_aux,2)  # ODOO SH
                resultado=valor*rate
            else:
                resultado=valor
        else:
            resultado=valor
        return resultado
   
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

    def integer_format(self,valor):
        result = '{:,.0f}'.format(valor)
        return result


    def fact_div_line(self,valor):
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.move_id.currency_id.id!=self.move_id.doc_currency_id.id:
            tasa= self.env['account.move'].search([('id','=',self.move_id.id)],order="id asc")
            for det_tasa in tasa:
                monto_nativo=det_tasa.amount_untaxed_signed
                monto_extran=det_tasa.amount_untaxed
                valor_aux=abs(monto_nativo/monto_extran)
            rate=round(valor_aux,3)  # LANTA
            #rate=round(valor_aux,2)  # ODOO SH
            resultado=valor*rate
        else:
            resultado=valor
        return resultado