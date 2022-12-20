from pickle import FALSE
from odoo  import models, fields, api

class wizardPrice(models.TransientModel):
    _name = "wizard.price" 

    product_ids = fields.Many2many('product.template', string='Productos')
    change = fields.Selection([('por', 'Porcentaje de ganancia'), ('fac', 'Factor de utilidad')])
    revenue = fields.Float(default=0.01)
    porc = fields.Integer()

    def recalculate_revenue(self):
        for det in self.product_ids:
            precio_dolar = det.cost_usd
            revenue = precio_dolar / self.revenue
            det.list_price_usd = revenue
            det.write({"calculation": "Factor de utilidad", "cant_r": self.revenue, "cant_p": False})
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
        }

    def recalculate_porc(self):
        for pro in self.product_ids:
            precio_dolar = pro.cost_usd
            porcentaje = precio_dolar * self.porc / 100
            pro.list_price_usd = pro.cost_usd + porcentaje
            pro.list_price = (pro.cost_usd + porcentaje)*pro.os_currency_rate
            pro.write({"calculation": "Porcentaje de ganancia", "cant_p": self.porc, "cant_r": False})
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
        }