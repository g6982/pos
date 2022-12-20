from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PosPaymentMeth(models.Model):
    _inherit = "pos.payment.method"

    """  
        no hago uso del campo 'split_transactions' nativo de odoo porque es usado
        para otro comportamiento en el sistema, el cual no necesariamente se desea
    """
    is_dollar_payment = fields.Boolean('Pago en USD')
    is_euro_payment = fields.Boolean('Pago en EURO')
    is_retend = fields.Boolean('Retencion IVA')
    percentage = fields.Float('% de retencion')

    @api.depends('journal_id', 'split_transactions')
    def _compute_type(self):
        for pm in self:
            if pm.journal_id.type in {'cash', 'bank'}:
                pm.type = pm.journal_id.type
            else:
                pm.type = 'pay_later'
