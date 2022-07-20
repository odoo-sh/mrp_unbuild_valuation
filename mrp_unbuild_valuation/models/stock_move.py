# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models, fields
from odoo.tools import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    created_from_mo_move_id = fields.Many2one(
        comodel_name="stock.move",
        copy=False,
    )

    def _create_out_svl(self, forced_quantity=None):
        res = self.env["stock.valuation.layer"]
        for move in self:
            move = move.with_context(svl_move=move)
            res |= super(StockMove, move)._create_out_svl(
                forced_quantity=forced_quantity
            )
        return res

    def _create_in_svl(self, forced_quantity=None):
        res = self.env["stock.valuation.layer"]
        for move in self:
            move = move.with_context(svl_move=move)
            res |= super(StockMove, move)._create_in_svl(
                forced_quantity=forced_quantity
            )
        return res

    def _get_price_unit(self):
        """Returns the unit price to value this stock move"""
        self.ensure_one()
        # If the move is an unbuild move, use the original move's price unit.
        if (
            self.created_from_mo_move_id
            and self.created_from_mo_move_id.sudo().stock_valuation_layer_ids
        ):
            layers = self.created_from_mo_move_id.sudo().stock_valuation_layer_ids
            quantity = sum(layers.mapped("quantity"))
            return (
                layers.currency_id.round(sum(layers.mapped("value")) / quantity)
                if not float_is_zero(
                    quantity, precision_rounding=layers.uom_id.rounding
                )
                else 0
            )
        return super()._get_price_unit()
