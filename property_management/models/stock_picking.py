from odoo import api, fields, models


class RegisterItemProperty(models.Model):
    _inherit = "stock.picking"

    reference_name = fields.Many2one('property', string="Property Destination")


