{
    'name': 'Smart Fan ERP',
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Custom ERP module for Smart Fan (Standard & Pro)',
    'description': """
        Smart Fan ERP
        ================
        This module configures Odoo for the Smart Fan production process.
        It includes:
        - Master data for Products, BOMs, and Reordering Rules
        - Custom approval flows for Manufacturing Orders
        - Custom security groups based on roles
    """,
    'author': 'Antigravity',
    'depends': [
        'base',
        'sale_management',
        'purchase',
        'mrp',
        'stock',
        'account',
    ],
    'data': [
        'data/product_category_data.xml',
        'data/product_data.xml',
        
        'data/initial_stock_data.xml',
        
        'data/bom_data.xml',
        'data/mto_route_setup.xml',
        'data/reordering_rules_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
