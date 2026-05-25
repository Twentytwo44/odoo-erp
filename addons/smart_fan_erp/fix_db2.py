import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    standard_fan = env.ref('smart_fan_erp.product_smart_fan_standard', raise_if_not_found=False)
    pro_fan = env.ref('smart_fan_erp.product_smart_fan_pro', raise_if_not_found=False)
    
    mto_route = env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
    mfg_route = env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
    buy_route = env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)

    if standard_fan:
        print("Standard old routes:", standard_fan.route_ids.mapped('name'))
        standard_fan.route_ids = [(6, 0, [mto_route.id, mfg_route.id])]
        print("Standard new routes:", standard_fan.route_ids.mapped('name'))
        
    if pro_fan:
        print("Pro old routes:", pro_fan.route_ids.mapped('name'))
        pro_fan.route_ids = [(6, 0, [mto_route.id, mfg_route.id])]
        print("Pro new routes:", pro_fan.route_ids.mapped('name'))

    cr.commit()
    print("Cleaned up routes to purely MTO + Manufacture!")
