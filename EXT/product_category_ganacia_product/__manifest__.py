# -*- coding: utf-8 -*-
{
    "name":"reporte de ganacias por producto v15",
    'category': 'inventory',
    "description":"Visualiza ganacias por rango de fecha",
    "author":"Ing.marilyn millan",
    "depends":['base','product', 'sale'],
    "data":[
        'security/ir.model.access.csv',
       # 'views/revenue_view.xml',
        'wizard/gain_product_view.xml',
    ]
}