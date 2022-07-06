# copyright 2022 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).

from odoo import models, fields, api


class MrpUnbuild(models.Model):
    _inherit = "mrp.unbuild"

    def _generate_move_from_existing_move(self, move, factor, location_id, location_dest_id):
        new_move = super()._generate_move_from_existing_move(move, factor, location_id, location_dest_id)
        new_move.write({
            'created_from_mo_move_id': move.id,
        })
        return new_move
