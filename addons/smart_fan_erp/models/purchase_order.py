# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        for order in self:
            if order.amount_total > 50000.0:
                is_manager = self.env.user.has_group('smart_fan_erp.group_fan_manager')
                
                is_admin = self.env.is_admin() or self.env.su
                
                if not (is_manager or is_admin):
                    raise UserError(_(
                        "🚨 Approval Required: This Purchase Order total exceeds 50,000 ฿. "
                        "Only users with Manager role permissions can confirm this transaction."
                    ))
                    
        return super(PurchaseOrder, self).button_confirm()