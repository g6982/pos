{
    "name": "Custom pintugama",
    "version": "15.0",
    "summary": "Custom Pintugama",
    "author": "marilyn millan",
    "license": "AGPL-3",
    "depends": ["base", "sales_team", "sale", "crm", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        # ----- vistas ------#
        "views/crm_sale_team.xml",
        "views/mrp_production.xml",
        "views/sale.xml",
        'views/product_template.xml',
        'views/stock_production_lot.xml',

        # ----- repotes ----- #
      
        "report/sale_report.xml",





    ],
    "installable": True,
    "auto_install": True,
    "application": False,
}