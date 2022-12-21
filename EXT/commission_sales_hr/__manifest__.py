# -*- coding: utf-8 -*-
{
    'name': "Comisiones por ventas",

    'summary': """
        Automatizacion de calculo de comisiones por factura pagada
    """,

    'description': """
        Automatizacion de calculo de comisiones por factura pagada
    """,

    'author': "marilyn millan",
    'contribuitors': "marilyn millan @millan2031@gmail.com>",
    'category': '',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll', 'sale', 'custom_pintugama','hr_campos_parametrizacion','l10n_ve_igtf_formato_libre', "crm"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale.xml',
        'views/account_move.xml',
        'views/hr_sales_commission.xml',
        #'views/hr_sales_goal.xml',
       # 'views/hr_inherit_payslip_view.xml',
       
        # ----- repotes ----- #
       # "report/sale_report.xml",


        # ----- wizards ----- #
       # "wizards/sale_report.xml",


   ],
    "installable": True,
    "auto_install": True,
    "application": False,
}