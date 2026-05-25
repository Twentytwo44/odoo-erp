import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Check RFQs
    rfqs = env['purchase.order'].search([('state', 'in', ['draft', 'sent', 'to approve'])])
    print("Pending RFQs:")
    for r in rfqs:
        print(f"- {r.name} for {r.partner_id.name}, Amount: {r.amount_total}")
        for line in r.order_line:
            print(f"  * {line.product_id.name}: {line.product_qty}")
            
    if not rfqs:
        print("No pending RFQs found.")
        
    # Check orderpoints (Reordering rules)
    print("\nReordering Rules:")
    orderpoints = env['stock.warehouse.orderpoint'].search([])
    for op in orderpoints:
        print(f"- {op.product_id.name}: Min={op.product_min_qty}, Multiple={op.qty_multiple}")
        
    # Check if BT module has vendor and buy route
    bt = env.ref('smart_fan_erp.product_bt_wifi_module', raise_if_not_found=False)
    if bt:
        print(f"\nBT Module Routes: {bt.route_ids.mapped('name')}")
        print(f"BT Module Vendors: {bt.seller_ids.mapped('partner_id.name')}")
