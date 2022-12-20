from odoo import fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    show_dual_currency      = fields.Boolean("Show dual currency", help="Show Other Currency in POS", default=True)
    rate_company            = fields.Float(string='Rate', related='currency_id.rate')
    show_currency           = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')], limit=1))
    show_currency_rate      = fields.Float(string='Rate', related='show_currency.rate')
    show_currency_rate_real = fields.Float(string='Rate', compute='_compute_tasa_real')

    show_currency_euro           = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'EUR')], limit=1))
    show_currency_rate_euro      = fields.Float(string='Rate', related='show_currency_euro.rate')
    show_currency_rate_real_euro = fields.Float(string='Rate', related='show_currency_euro.sell_rate')

    show_currency_symbol    = fields.Char(related='show_currency.symbol')
    show_currency_position  = fields.Selection([('after', 'After'),('before', 'Before'),],related='show_currency.position')
    default_location_src_id = fields.Many2one("stock.location", related="picking_type_id.default_location_src_id")

    def _compute_tasa_real(self):
        self.show_currency_rate_real=(1/self.show_currency_rate)
