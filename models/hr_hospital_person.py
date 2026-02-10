from odoo import models, fields


class Person(models.AbstractModel):
    """Abstract model to store common personal information."""
    _name = 'hr.hospital.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    # Full Name details
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    middle_name = fields.Char(string='Middle Name')

    # Computed Full Name (Logic will be added in step 6.2)
    full_name = fields.Char(
        string='Full Name',
        store=True
    )

    # Contact Information
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    # Personal Details
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        string='Gender',
        default='male'
    )
    birthday = fields.Date(string='Date of Birth')

    # Computed Age (Logic will be added in step 6.2)
    age = fields.Integer(
        string='Age',
        readonly=True
    )

    # Relations
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship'
    )
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Language'
    )