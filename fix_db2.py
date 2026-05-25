import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    standard_fan = env.ref('smart_fan_erp.product_smart_fan_standard', raise_if_not_found=False)
    pro_fan = env.ref('smart_fan_erp.product_smart_fan_pro', raise_if_not_found=False)
    if standard_fan:
        print("Standard routes:", standard_fan.route_ids.mapped('name'))
        buy_route = env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route and buy_route in standard_fan.route_ids:
            standard_fan.route_ids = [(3, buy_route.id)]
            print("Removed Buy route from Standard")
    if pro_fan:
        print("Pro routes:", pro_fan.route_ids.mapped('name'))
        buy_route = env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route and buy_route in pro_fan.route_ids:
            pro_fan.route_ids = [(3, buy_route.id)]
            print("Removed Buy route from Pro")
    cr.commit()
