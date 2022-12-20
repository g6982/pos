# -*- coding: utf-8 -*-
{
    'name': "Personalizacion Lanta",

    'summary': """Personalizacion Lanta""",

    'description': """
       Personalizacion Lanta
    """,
    'version': '3.0',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'category': 'Tools',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_accountant','vat_retention'],

    # always loaded
    'data': [
        'view/vista_view.xml',
    ],
    'application': True,
}
