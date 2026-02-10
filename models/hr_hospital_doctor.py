from odoo import models, fields


class Doctor(models.Model):
    """Model to manage doctor information, inheriting from abstract person."""
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = 'hr.hospital.person'

    # System integration
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
        help='User account for system login'
    )

    # Professional information
    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.specialty',
        string='Specialty'
    )
    is_intern = fields.Boolean(
        string='Is Intern',
        default=False
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor Doctor',
        help='Available only for interns'
    )

    # Licensing and experience
    license_number = fields.Char(
        string='License Number',
        required=True,
        copy=False
    )
    license_date = fields.Date(string='License Issue Date')

    # Computed Experience (Logic will be added in step 6.2)
    experience = fields.Integer(
        string='Work Experience (Years)',
        readonly=True
    )

    # Ratings and Schedule
    rating = fields.Float(
        string='Rating',
        digits=(3, 2),
        help='Doctor rating from 0.00 to 5.00'
    )
    schedule_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string='Work Schedule'
    )

    # Education
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Study'
    )
