# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    created_from_mo_move_id = fields.Many2one(
        comodel_name="stock.move",
        copy=False,
    )
