from odoo import api, fields, models


class RegiserRegion(models.Model):
    _name = "mcit.property.region"
    _description = "hr type module"
    _rec_name = "Region_Name"

    Region_Name = fields.Char(string='Region Name', required=True)
