from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class Person(models.AbstractModel):
    """Abstract model to store common personal information."""
    _name = 'hr.hospital.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    # Full Name details
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    middle_name = fields.Char(string='Middle Name')

    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name',
        store=True  # Store in DB for search and sorting
    )

    # Contact Information
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        string='Gender',
        default='male'
    )

    # Personal Details
    birthday = fields.Date(string='Date of Birth')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        help='Calculated age based on birthday'
    )

    # Computed Age (Logic will be added in step 6.2)
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship'
    )

    # Relations
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Language'
    )

    # age depends on birthday
    # to check age we must check birthday
    @api.constrains('birthday')
    def _check_birthday(self):
        for person in self:
            if person.birthday > fields.Date.today():
                raise ValidationError(_("Birthday cannot be in the future!"))
            if person.birthday == fields.Date.today():
                raise ValidationError(_("The person must be at least one day old!"))


    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_full_name(self):
        for person in self:
            name_parts = [person.last_name, person.first_name, person.middle_name]
            person.full_name = " ".join([part for part in name_parts if part])

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for person in self:
            if person.birthday:
                diff = relativedelta(today, person.birthday)
                person.age = diff.years
            else:
                person.age = 0

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            self.lang_id = self.country_id.default_lang_id
