import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo-db', '--db_host', 'db', '--db_user', 'odoo', '--db_password', 'odoo'])
registry = odoo.registry('odoo-db')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    p = env['product.product'].search([('name', 'ilike', 'Smart Fan Standard')], limit=1)
    if p:
        print("Product:", p.name, "Type:", p.type)
        print("Routes:", p.route_ids.mapped('name'))
        mto = env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        print("MTO Route exists?", bool(mto), "Active?", mto.active if mto else False)
        mfg = env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
        print("MFG Route exists?", bool(mfg), "Active?", mfg.active if mfg else False)
    else:
        print("Product not found")
