from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    next_days_defeat = fields.Integer(string='Dias para proximo a vencer')
    lot_state = fields.Char(string='Estado del lote', compute='_compute_next_days_defeat_lot')
    next_defeat_bool = fields.Boolean(string='proximo a vencerse', default=False)
    defeat_bool = fields.Boolean(string='Vencido', default=False)
    avalaible_bool = fields.Boolean(string='Disponible', default=False)
    
    @api.depends('expiration_date')
    def _compute_next_days_defeat_lot(self):
        current_date = fields.Datetime.now()
        for lot in self:
            if lot.expiration_date:
                if lot.expiration_date.day <= current_date.day and lot.expiration_date.month <= current_date.month and lot.expiration_date.year <= current_date.year:
                    lot.defeat_bool = True
                    lot.lot_state = 'Vencido'
                else:
                    if lot.next_days_defeat == 0 and lot.expiration_date.day <= current_date.day and lot.expiration_date.month <= current_date.month and lot.expiration_date.year <= current_date.year:
                        lot.defeat_bool = True
                        lot.lot_state = 'Vencido'
                    if lot.next_days_defeat:
                        days = lot.next_days_defeat
                        result_date = current_date - lot.expiration_date
                        if abs(result_date) <= timedelta(days=days):
                            lot.next_defeat_bool = True
                            lot.lot_state = 'Proximo a vencerse'
                        if abs(result_date) > timedelta(days=days):
                            lot.avalaible_bool = True
                            lot.lot_state = 'Disponible'
                        # else:
                        #     if current_date == lot.expiration_date:
                        #         lot.defeat_bool = True
                        #         lot.lot_state = 'Vencido'
                    else:
                        lot.lot_state = 'Disponible'
            else:
                lot.lot_state = ''
                
                
    @api.onchange('next_days_defeat')
    def onchange_days_defeat_lot(self):
        current_date = fields.Datetime.now()
        for lot in self:
            if lot.expiration_date:
                if lot.expiration_date.day <= current_date.day and lot.expiration_date.month <= current_date.month and lot.expiration_date.year <= current_date.year:
                    lot.defeat_bool = True
                    lot.lot_state = 'Vencido'
                else:
                    if lot.next_days_defeat == 0 and lot.expiration_date.day <= current_date.day and lot.expiration_date.month <= current_date.month and lot.expiration_date.year <= current_date.year:
                        lot.defeat_bool = True
                        lot.lot_state = 'Vencido'
                    if lot.next_days_defeat:
                        days = lot.next_days_defeat
                        result_date = current_date - lot.expiration_date
                        if abs(result_date) <= timedelta(days=days):
                            lot.next_defeat_bool = True
                            lot.lot_state = 'Proximo a vencerse'
                        if abs(result_date) > timedelta(days=days):
                            lot.avalaible_bool = True
                            lot.lot_state = 'Disponible'
                        # else:
                        #     if current_date == lot.expiration_date:
                        #         lot.defeat_bool = True
                        #         lot.lot_state = 'Vencido'
                    else:
                        lot.lot_state = 'Disponible'
            else:
                lot.lot_state = ''

    
   