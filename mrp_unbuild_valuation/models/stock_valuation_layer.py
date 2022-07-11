# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            move_id = vals.get("stock_move_id", False)
            if not move_id:
                continue
            move = self.env["stock.move"].browse(move_id)
            if move.unbuild_id and move.created_from_mo_move_id:
                company_id = self.env.context.get("force_company", self.env.company.id)
                company = self.env["res.company"].browse(company_id)
                quantity = vals.get("quantity", 0) if vals.get("quantity", 0) else 0
                remaining_qty = vals.get("remaining_qty", 0) if vals.get("remaining_qty", 0) else 0
                valuation = self.env["stock.valuation.layer"].search(
                    [("stock_move_id", "=", move.created_from_mo_move_id.id)],
                    limit=1,
                    order="id",
                )
                if not valuation:
                    continue
                vals.update(
                    {
                        "value": company.currency_id.round(
                            valuation.unit_cost * quantity
                        ),
                        "unit_cost": valuation.unit_cost,
                        "remaining_value": company.currency_id.round(
                            valuation.unit_cost * remaining_qty
                        ),
                    }
                )
        return super().create(vals_list)
