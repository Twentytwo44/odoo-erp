from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    state = fields.Selection(selection_add=[
        ('to_approve', 'To Approve')
    ], ondelete={'to_approve': lambda r: r.write({'state': 'draft'})})

    def button_plan(self):
        # Intercept the plan button.
        # If product quantity > 100, we require manager approval.
        for production in self:
            if production.product_qty > 100 and production.state == 'draft':
                production.state = 'to_approve'
                return True
        return super(MrpProduction, self).button_plan()

    def button_mark_done(self):
        # Alternatively, intercept mark done if it's not planned
        for production in self:
            if production.product_qty > 100 and not self.env.user.has_group('mrp.group_mrp_manager'):
                raise UserError(_('Manufacturing orders over 100 units require Production Manager approval.'))
        return super(MrpProduction, self).button_mark_done()

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group('mrp.group_mrp_manager'):
            raise UserError(_('Only Production Managers can approve this order.'))
        self.state = 'confirmed'
        return self.button_plan()
