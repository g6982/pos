# -*- coding: utf-8 -*-
{
        'name': ' Venezuela - Sucursal Purchase',
        'version': '14.0.1.0',
        'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
        'contribuitors': "Bryan Gómez <bryan.gomez1311@gmail.com>",
        'summary': '',
        'description': """""",
        'category': 'Accounting/Localizations/Account Charts',
        'website': 'http://soluciones-tecno.com/',
        'depends': [
                'l10n_ve_sucursal',
                'l10n_ve_sucursal_stock',
                'l10n_ve_sucursal_account_analytic',
                'purchase_stock',
                'purchase'
        ],
        'data': ['views/purchase_views.xml'],
        'license': 'LGPL-3',
        'installable': True,
        'application': True,
        'auto_install': False,
                      
}
