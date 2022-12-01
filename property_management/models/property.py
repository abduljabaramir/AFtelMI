from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _name = "property"
    _description = "Property"
    _rec_name = "display_name"

    reference_name = fields.Char(compute='_compute_reference_name', recursive=True, store=True, index=True)
    reference_no = fields.Char(string='Order Reference', required=True, readonly=True, default='New')
    name = fields.Char('Name', required=True)
    display_name = fields.Char(compute='_compute_display_name', recursive=True, copy=False, store=True, index=True)
    active = fields.Boolean(default=True)
    is_root = fields.Boolean(default=True)
    area = fields.Float('Area')
    no_of_floor = fields.Integer(string="Number of Floors", compute='_compute_no_of_floor', store=True)
    no_of_room = fields.Integer(string="Number of Rooms", compute='_compute_no_of_room', store=True)
    no_of_bathroom = fields.Integer(string="Number of Bathroom", compute='_compute_no_of_bathroom', store=True)
    no_of_hall = fields.Integer(string="Number of Hall", compute='_compute_no_of_hall', store=True)

    type = fields.Selection([
        ('property', 'Property'),
        ('site', 'Site')
    ], string='Type')

    property_type = fields.Selection([
        ('land', 'Land'),
        ('yard', 'Yard'),
        ('building', 'Building')
    ], string='Property Type')
    building_type = fields.Selection([
        ('pokhta', 'Pokhta'),
        ('nim-pokhta', 'Nim Pokhta'),
        ('khama', 'Khama')
    ], string='Building Type')
    building_part = fields.Selection([
        ('room', 'Room'),
        ('bathroom', 'Bathroom'),
        ('hall', 'Hall'),
        ('floor', 'Floor'),
    ], string='Building Part')

    parent_id = fields.Many2one('property', string='Parent', index=True)
    child_ids = fields.One2many('property', 'parent_id', string='Parts')
    property_uom = fields.Many2one('uom.uom', "UoM")
    site_number = fields.Char()
    region_id = fields.Many2one("mcit.property.region", string="Region Name")
    province_id = fields.Many2one("mcit.property.province", string="Province Name")
    district_id = fields.Many2one("mcit.property.district", string="District Name")
    Nahya = fields.Char(string="Nahya Name")
    Qarya = fields.Char(string="Qarya Name")
    typeof_lessor = fields.Selection(string="Lessor Type",
                                     selection=[('rent', 'Rent'), ('gov', 'Government'), ('free', 'Free'),
                                                ('share', 'Share')])
    lessor_name = fields.Char(string="Name")
    lessor_fname = fields.Char(string="F/Name")
    phone_no = fields.Char(string="Phone No")
    name_company = fields.Char(string="Company Name")
    monthly_rent = fields.Integer(string="Monthly Rent")
    monetary_unit = fields.Selection(string="Monetary Unit", selection=[('afg', 'Afg'), ('usd', 'USD')])
    bank_account = fields.Char(string="Bank Account")
    bank_name = fields.Char(string="Bank")
    contract_start_date = fields.Date(string="Start Date")
    contract_end_date = fields.Date(string="End Date")

    no_qabalah = fields.Char(string='no_qabala')
    shumara_e_Qetah = fields.Char(string='shumara_e_qetah')
    Grade_Qetah = fields.Char(string='Grade_Qetah')
    Number_e_kadistari = fields.Char(string='number_e_kadistari')
    Registration_no = fields.Char()
    Qemat_Property = fields.Char()
    Owner_of_property = fields.Char()

    North = fields.Char(string="North side")
    South = fields.Char(string="South Side")
    West = fields.Char(string="West side")
    East = fields.Char(string="East side")

    @api.onchange("region_id")
    def load_related_province(self):
        for rec in self:
            return {
                'domain': {'province_id': [('Region_id', '=', rec.region_id.id)]}
            }

    @api.onchange("province_id")
    def load_related_district(self):
        for rec in self:
            return {
                'domain': {'district_id': [('province_id', '=', rec.province_id.id)]}

            }

    @api.depends('name', 'parent_id.display_name')
    def _compute_display_name(self):
        for prop in self:
            if prop.parent_id:
                prop.display_name = '%s/%s' % (prop.parent_id.display_name, prop.name)
            else:
                prop.display_name = prop.name

    @api.model
    def create(self, vals):
        if vals.get('reference_no', 'New') == 'New':
            vals['reference_no'] = self.env['ir.sequence'].next_by_code('property') or 'New'
        res = super(Property, self).create(vals)
        return res

    # @api.onchange('child_ids')
    # def _onchange_child_ids(self):
    #     total_floor = 0
    #     total_room = 0
    #     total_bathroom = 0
    #     total_hall = 0
    #
    #     for child in self.child_ids:
    #         if child.building_part == 'floor':
    #             total_floor += 1
    #             total_bathroom += child.no_of_bathroom
    #             total_room += child.no_of_room
    #             total_hall += child.no_of_hall
    #         if child.building_part == 'room':
    #             total_room += 1
    #         if child.building_part == 'bathroom':
    #             total_bathroom += 1
    #         if child.building_part == 'hall':
    #             total_hall += 1
    #
    #     self.no_of_floor = total_floor
    #     self.no_of_room = total_room
    #     self.no_of_bathroom = total_bathroom
    #     self.no_of_hall = total_hall

    @api.depends('child_ids')
    def _compute_no_of_floor(self):
        for rec in self:
            floors = 0
            rooms = 0
            bathrooms = 0
            halls = 0

            for child in rec.child_ids:
                if child.building_part == 'floor':
                    floors += 1
                    rooms += child.no_of_room
                    bathrooms += child.no_of_bathroom
                    halls += child.no_of_hall
                if child.building_part == 'room':
                    rooms += 1
                if child.building_part == 'bathroom':
                    bathrooms += 1
                if child.building_part == 'hall':
                    halls += 1
            rec.no_of_floor = floors
            rec.no_of_room = rooms
            rec.no_of_bathroom = bathrooms
            rec.no_of_hall = halls

    @api.depends('child_ids')
    def _compute_no_of_room(self):
        for rec in self:
            total = 0
            for child in rec.child_ids:
                if child.building_part == 'room':
                    total += 1
            rec.no_of_room = total

    @api.depends('child_ids')
    def _compute_no_of_bathroom(self):
        for rec in self:
            total = 0
            for child in rec.child_ids:
                if child.building_part == 'bathroom':
                    total += 1
            rec.no_of_bathroom = total

    @api.depends('child_ids')
    def _compute_no_of_hall(self):
        for rec in self:
            total = 0
            for child in rec.child_ids:
                if child.building_part == 'hall':
                    total += 1
            rec.no_of_hall = total
