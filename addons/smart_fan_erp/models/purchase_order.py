from odoo import models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        for order in self:
            # Overriding to ensure that if amount > 50,000, it goes to 'to approve'
            # Odoo natively has a setting for this: 'po_double_validation' = 'two_step'
            # and 'po_double_validation_amount'
            # We enforce it here programmatically based on the PDF requirement
            if order.amount_total > 50000 and order.state in ['draft', 'sent']:
                order.write({'state': 'to approve'})
                return True
        return super(PurchaseOrder, self).button_confirm()
