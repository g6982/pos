# -*- coding: utf-8 -*-
{
    "name":"Actualizador de coste de ganancias por producto v15",
    'category': 'inventory',
    "description":"Actuliza el coste de ganancias de cada producto",
    "author":"",
    "depends":['base','product', 'sale'],
    "data":[
        'security/ir.model.access.csv',
        'views/revenue_view.xml',
        'wizard/end_price_view.xml',
    ]
}