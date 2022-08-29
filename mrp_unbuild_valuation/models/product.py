# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models
from odoo.tools import float_compare, float_is_zero


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _run_fifo(self, quantity, company):
        vals = super()._run_fifo(quantity, company)
        svl_move = self.env.context.get("svl_move")
        if svl_move and svl_move.created_from_mo_move_id:
            origin_move = svl_move.created_from_mo_move_id
            origin_move_layers = origin_move.sudo().stock_valuation_layer_ids
            layers_qty = sum(origin_move_layers.mapped("quantity"))
            layers_value = sum(origin_move_layers.mapped("value"))
            layer_currency_id = origin_move_layers and origin_move_layers[0].currency_id
            layer_precision = origin_move_layers and origin_move_layers[0].uom_id.rounding
            unit_cost = layer_currency_id.round(layers_value / layers_qty) if not float_is_zero(layers_qty, precision_rounding=layer_precision) else 0
            vals.update({
                "unit_cost": unit_cost,
                "value": unit_cost * quantity * -1
            })
        return vals
