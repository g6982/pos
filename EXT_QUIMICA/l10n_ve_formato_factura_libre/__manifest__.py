# -*- coding: utf-8 -*-
{
    'name': "FORMATO_LIBRE_QUIMICA_PARA_LA_VIDA",

    'summary': """Formato LIBRE QUIMICA PARA LA VIDA""",

    'description': """  Formato libre de quimica parala vida y campo de observacion """,
    'version': '15',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'category': 'Tools',
    'website': 'http://soluciones-tecno.com/',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'formatos/factura_libre_quimica.xml',
        'formatos/account_move.xml'

    ],
    'application': True,
    'active':False,
    'auto_install': False,
}
