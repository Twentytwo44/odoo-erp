import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Get or create vendor
    vendor = env['res.partner'].search([('name', '=', 'Electronic Parts Supplier Co.')], limit=1)
    if not vendor:
        vendor = env['res.partner'].create({
            'name': 'Electronic Parts Supplier Co.',
            'is_company': True,
        })
        
    buy_route = env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
    
    components = [
        'smart_fan_erp.product_bt_wifi_module',
        'smart_fan_erp.product_motor',
        'smart_fan_erp.product_blade',
        'smart_fan_erp.product_grill',
        'smart_fan_erp.product_fan_base',
        'smart_fan_erp.product_control_board',
        'smart_fan_erp.product_remote',
        'smart_fan_erp.product_temp_sensor'
    ]
    
    for comp_ref in components:
        comp = env.ref(comp_ref, raise_if_not_found=False)
        if comp:
            # 1. Add Buy Route
            if buy_route:
                comp.route_ids = [(4, buy_route.id)]
                
            # 2. Add Vendor if missing
            if not env['product.supplierinfo'].search([('product_tmpl_id', '=', comp.product_tmpl_id.id), ('partner_id', '=', vendor.id)]):
                env['product.supplierinfo'].create({
                    'partner_id': vendor.id,
                    'product_tmpl_id': comp.product_tmpl_id.id,
                    'min_qty': 500.0 if 'bt_wifi' in comp_ref else 100.0,
                    'price': 100.0,
                })
                
    cr.commit()
    print("Fixed components: added Buy route and Vendor.")
    
    # Run the scheduler to trigger PO generation for the negative stock!
    try:
        env['procurement.group'].run_scheduler()
        cr.commit()
        print("Scheduler ran successfully. POs should now be generated.")
    except Exception as e:
        print("Error running scheduler:", str(e))
