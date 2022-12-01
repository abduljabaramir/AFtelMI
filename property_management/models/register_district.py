from odoo import api, fields, models


class RegisterDistrict(models.Model):
    _name = "mcit.property.district"
    _description = "hr type module"
    _rec_name = "District_Name"

    District_Name = fields.Char(string='District Name', required=True)
    province_id = fields.Many2one("mcit.property.province", string="Province Name", required=True)
