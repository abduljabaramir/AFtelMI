from odoo import api, fields, models


class RegisterProvince(models.Model):
    _name = "mcit.property.province"
    _description = "hr type module"
    _rec_name = "Province_Name"

    Province_Name = fields.Char(string='Province Name', required=True)
    Region_id = fields.Many2one("mcit.property.region", string="Region Name", required=True)
