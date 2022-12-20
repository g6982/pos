# -*- coding: utf-8 -*-

from odoo import models, fields, _

class ResCompany(models.Model):

    _inherit = 'res.company'

    allow_warehouse = fields.Boolean(string="Allow Warehouse in Sale Order Line", default=False)