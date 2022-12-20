# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class PortalAccount(PortalAccount):

    @http.route(['/my/invoices/natural/<string:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail_natural(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        pos = http.request.env['pos.order'].sudo().search([('pos_reference', '=', invoice_id)])
        invoice_sudo = pos.account_move
        return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='naida_hogar_module_extend.action_factura_pdv_naida', download=download)

    @http.route(['/my/invoices/nota/<string:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail_nota(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        pos = http.request.env['pos.order'].sudo().search([('pos_reference', '=', invoice_id)])
        invoice_sudo = pos.account_move
        return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='naida_hogar_module_extend.action_nota_entrega_pdv_naida', download=download)
