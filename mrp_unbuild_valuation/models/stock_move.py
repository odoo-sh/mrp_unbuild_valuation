# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    created_from_mo_move_id = fields.Many2one(
        comodel_name="stock.move",
        copy=False,
    )

    def _prepare_in_svl_vals(self, quantity, unit_cost):
        if self.unbuild_id and self.created_from_mo_move_id:
            valuation = self.env['stock.valuation.layer'].search([('stock_move_id', '=', self.created_from_mo_move_id.id)], limit=1, order="id")
            unit_cost = valuation.unit_cost
        return super()._prepare_in_svl_vals(quantity, unit_cost)

    def _prepare_out_svl_vals(self, quantity, company):
        vals = super(). _prepare_out_svl_vals(quantity, company)
        company_id = self.env.context.get('force_company', self.env.company.id)
        company = self.env['res.company'].browse(company_id)
        if self.unbuild_id and self.created_from_mo_move_id:
            valuation = self.env['stock.valuation.layer'].search([('stock_move_id', '=', self.created_from_mo_move_id.id)], limit=1, order="id")
            vals.update({
                'value': company.currency_id.round(valuation.unit_cost * quantity),
                'unit_cost': valuation.unit_cost,
            })
        return vals
