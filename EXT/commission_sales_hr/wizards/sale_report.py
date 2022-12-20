from sqlite3 import Date
import xlrd

import xlwt
import base64
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from io import BytesIO
import logging
from calendar import monthrange
from dateutil.relativedelta import relativedelta


class SaleReport(models.TransientModel):
    _name = 'sale.report.excel'
    _description = 'Sale Report Excel'
    
    product_ids = fields.Many2many('product.product', string='Productos')
    date_start = fields.Date(string='Desde')
    date_stop = fields.Date(string="Hasta")
    period_selection = fields.Selection([('null', ' '),
                                         ('annual', 'Anual'),
                                         ('semiannual', 'Semestral'),
                                         ('bimonthly', 'Bimestral'),
                                         ('monthly', 'Mensual'),
                                         ('daily', 'Diario')], string='Periodo a filtrar')
    

    @api.onchange('period_selection')
    def period_selection_onchange(self):
        if self.period_selection == 'annual':
            self.date_stop = self.date_start + relativedelta(years=1)

        if self.period_selection == 'semiannual':
            self.date_stop = self.date_start + relativedelta(months=6)
        
        if self.period_selection == 'bimonthly':
            self.date_stop = self.date_start + relativedelta(months=2)

        if self.period_selection == 'monthly':
            self.date_stop = self.date_start + relativedelta(months=1)
            # month = monthrange(self.date_start.year, self.date_start.month)[1]
            # self.date_stop = self.date_start + month
        if self.period_selection == 'daily':
            self.date_stop = self.date_start + timedelta(days=1)

    def generate_report_sale_xlsx(self):

        workbook = xlwt.Workbook(encoding="utf-8")
        sheet = workbook.add_sheet("Clientes y Ventas")
        today = datetime.now().date()
        file_name = "Clientes y Ventas " + str(today)
        sheet.write(0, 0, 'Fecha')
        sheet.write(0, 1, 'Nombre')
        sheet.write(0, 2, 'Vendedor')
        sheet.write(0, 3, 'Ciudad')
        sheet.write(0, 4, 'Pais')
        sheet.write(0, 5, 'Region')
        sheet.write(0, 6, 'Producto')
        sheet.write(0, 7, 'Unidades')
        sheet.write(0, 8, 'Monto Unitario')
        sheet.write(0, 9, 'Moneda')
        sheet.write(0, 10, 'Total')
        
        line = 1

        sale = self.env['sale.order'].search([('date_order', '>=', self.date_start), ('date_order', '<=', self.date_stop)])
        sale_list = []
        if sale:
            if self.product_ids:
                for s in sale:
                    for sl in s.order_line.filtered(lambda pl: pl.product_id.id in self.product_ids.ids):
                            sale_dict = {
                                        'date_order': s.date_order,
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

                for sales in sale_list:
                    sheet.write(line, 0, sales['date_order'].strftime('%d-%m-%Y')) # Fecha
                    sheet.write(line, 1, sales['partner_id']) # Nombre
                    sheet.write(line, 2, sales['repre_sale']) #  Vendedor
                    sheet.write(line, 3, sales['city']) # Ciudad
                    sheet.write(line, 4, sales['country_id']) # Pais
                    sheet.write(line, 5, sales['state_id']) # Region
                    sheet.write(line, 6, sales['product_id']) # Producto
                    sheet.write(line, 7, sales['product_qty']) # Venta Unid
                    sheet.write(line, 8, sales['amount']) # Monto
                    sheet.write(line, 9, sales['currency_id']) # Moneda
                    sheet.write(line, 10, sales['amount_total']) # Total


                    line += 1
                    
                    
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

                for sales in sale_list:
                    
                    sheet.write(line, 0, sales['date_order'].strftime('%d-%m-%Y')) # Fecha
                    sheet.write(line, 1, sales['partner_id']) # Nombre
                    sheet.write(line, 2, sales['repre_sale']) #  Vendedor
                    sheet.write(line, 3, sales['city']) # Ciudad
                    sheet.write(line, 4, sales['country_id']) # Pais
                    sheet.write(line, 5, sales['state_id']) # Region
                    sheet.write(line, 6, sales['product_id']) # Producto
                    sheet.write(line, 7, sales['product_qty']) # Venta Unid
                    sheet.write(line, 8, sales['amount']) # Monto
                    sheet.write(line, 9, sales['currency_id']) # Moneda
                    sheet.write(line, 10, sales['amount_total']) # Total


                    line += 1


        if not self.date_start and not self.date_stop and self.product_ids:
            sale = self.env['sale.order'].search([])
            [data] = self.read()
            sale_list = []
            for s in sale:
                for sl in s.order_line.filtered(lambda pl: pl.product_id.id in self.product_ids.ids):
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
                        
            # workbook = xlwt.Workbook(encoding="utf-8")
            # sheet = workbook.add_sheet("Clientes y Ventas")
            # today = datetime.now().date()
            # file_name = "Clientes y Ventas " + str(today)
            # sheet.write(0, 0, 'Nombre')
            # sheet.write(0, 1, 'Vendedor')
            # sheet.write(0, 2, 'Ciudad')
            # sheet.write(0, 3, 'Pais')
            # sheet.write(0, 4, 'Region')
            # sheet.write(0, 5, 'Producto')
            # sheet.write(0, 6, 'Venta Unid')
            # sheet.write(0, 7, 'Monto')
            # sheet.write(0, 8, 'Total')


            # line = 1

            for sales in sale_list:
                sheet.write(line, 0, sales['date_order'].strftime('%d-%m-%Y')) # Fecha
                sheet.write(line, 1, sales['partner_id']) # Nombre
                sheet.write(line, 2, sales['repre_sale']) #  Vendedor
                sheet.write(line, 3, sales['city']) # Ciudad
                sheet.write(line, 4, sales['country_id']) # Pais
                sheet.write(line, 5, sales['state_id']) # Region
                sheet.write(line, 6, sales['product_id']) # Producto
                sheet.write(line, 7, sales['product_qty']) # Venta Unid
                sheet.write(line, 8, sales['amount']) # Monto
                sheet.write(line, 9, sales['currency_id']) # Moneda
                sheet.write(line, 10, sales['amount_total']) # Total


                line += 1
                
                
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

            for sales in sale_list:
                
                sheet.write(line, 0, sales['date_order'].strftime('%d-%m-%Y')) # Fecha
                sheet.write(line, 1, sales['partner_id']) # Nombre
                sheet.write(line, 2, sales['repre_sale']) #  Vendedor
                sheet.write(line, 3, sales['city']) # Ciudad
                sheet.write(line, 4, sales['country_id']) # Pais
                sheet.write(line, 5, sales['state_id']) # Region
                sheet.write(line, 6, sales['product_id']) # Producto
                sheet.write(line, 7, sales['product_qty']) # Venta Unid
                sheet.write(line, 8, sales['amount']) # Monto
                sheet.write(line, 9, sales['currency_id']) # Moneda
                sheet.write(line, 10, sales['amount_total']) # Total

                line += 1


        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodestring(data)
        doc = self.env['ir.attachment'].create({
            'name': '%s.xls' % (file_name),
            'datas': data_b64,
            'store_fname': '%s.xls' % (file_name),
            'type': 'url'
        })
        return {
            'type': "ir.actions.act_url",
            'url': "web/content/?model=ir.attachment&id=" + str(
                doc.id) + "&filename_field=datas_fname&field=datas&download=true&filename=" + str(doc.name),
            'target': "current",
            'no_destroy': False,
        }


    def print_report_sale(self):
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

        return self.env.ref('commission_sales_hr.action_report_sale').report_action(sale, data=data)