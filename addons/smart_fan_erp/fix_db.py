import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Unarchive MTO route
    mto_route = env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
    if mto_route:
        mto_route.active = True
        print("MTO Route activated!")
        
    mfg_route = env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
    
    # 2. Update finished products (Standard and Pro)
    standard_fan = env.ref('smart_fan_erp.product_smart_fan_standard', raise_if_not_found=False)
    if standard_fan and mto_route and mfg_route:
        standard_fan.route_ids = [(4, mto_route.id), (4, mfg_route.id)]
        print("Updated Standard Fan routes!")
        
    pro_fan = env.ref('smart_fan_erp.product_smart_fan_pro', raise_if_not_found=False)
    if pro_fan and mto_route and mfg_route:
        pro_fan.route_ids = [(4, mto_route.id), (4, mfg_route.id)]
        print("Updated Pro Fan routes!")
        
    # 3. Update component (Bluetooth Module)
    bt_module = env.ref('smart_fan_erp.product_bt_wifi_module', raise_if_not_found=False)
    vendor = env.ref('smart_fan_erp.vendor_electronic_parts', raise_if_not_found=False)
    
    if bt_module and vendor:
        # Check if supplierinfo exists
        if not env['product.supplierinfo'].search([('product_tmpl_id', '=', bt_module.product_tmpl_id.id), ('partner_id', '=', vendor.id)]):
            env['product.supplierinfo'].create({
                'partner_id': vendor.id,
                'product_tmpl_id': bt_module.product_tmpl_id.id,
                'min_qty': 500.0,
                'price': 100.0,
            })
            print("Added vendor info for BT Module")
            
        buy_route = env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route:
            bt_module.route_ids = [(4, buy_route.id)]
            print("Added Buy route to BT Module")

    cr.commit()
    print("Database updated successfully.")
