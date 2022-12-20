# -*- coding: utf-8 -*-
{
    'name': "Extencion Terminal Punto de Venta",

    'summary': """Extencion Terminal Punto de Venta""",

    'description': """
       Extencion Terminal Punto de Venta
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Extension Módulo Terminal Punto de Venta',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'point_of_sale',
        #'l10n_ve_fiscal_requirements',
        'account',
        #'ext_base_impuesto_tpdv'
        ],

    # always loaded
    'data': [
        'vista/buttom_menu_view.xml',
        'vista/vista_tax_view.xml',
        'vista/vista_pos_paymet_inheret.xml',
        'vista/vista_pos_order_inherit.xml',
        'vista/pos_config_inherit.xml',
        #'vista/vista_session_inherit.xml',
        'security/ir.model.access.csv',
        'reports/report_libro_pos.xml',
        'wizards/wizard_libro_ventas_pos.xml',
        #'wizards/reimpresionfiscal.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
