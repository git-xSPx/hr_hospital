from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil.relativedelta import relativedelta

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
    # Field to store where the doctor received their education
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Education',
        help='The country where the doctor obtained their medical degree'
    )
    is_intern = fields.Boolean(
        string='Is Intern',
        default=False
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor Doctor',
        domain="[('is_intern', '=', False)]",
        help='Available only for interns'
    )

    # Licensing and experience
    license_number = fields.Char(
        string='License Number',
        required=True,
        copy=False
    )

    license_date = fields.Date(string='License Issue Date')

    experience = fields.Integer(
        string='Work Experience (Years)',
        compute='_compute_experience',
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

    _license_number_unique = models.Constraint(
        'UNIQUE(license_number)',
        'The license number must be unique!')

    _check_rating = models.Constraint(
        'CHECK(rating >= 0 AND rating <= 5)',
        'The doctor rating must be between 0 and 5.00!',
    )

    # _sql_constraints = [
    #     ('license_number_unique',
    #      'unique(license_number)',
    #      'The license number must be unique!'),
    #
    #     ('check_rating',
    #      'CHECK(rating >= 0 AND rating <= 5)',
    #      'The doctor rating must be between 0.00 and 5.00!')
    # ]

    @api.constrains('is_intern', 'mentor_id')
    def _check_mentor_not_intern(self):
        for doctor in self:
            if doctor.is_intern and doctor.mentor_id:
                if doctor.mentor_id.is_intern:
                    raise ValidationError(_("An intern cannot be a mentor for another intern!"))
                if doctor.mentor_id == doctor:
                    raise ValidationError(_("A doctor cannot be their own mentor!"))

    def action_archive(self):
        for doctor in self:
            scheduled_visits_count = self.env['hr.hospital.visit'].search_count([
                ('doctor_id', '=', doctor.id),
                ('state', '=', 'scheduled')
            ])
            if scheduled_visits_count > 0:
                raise UserError(_(
                    "You cannot archive doctor %s because they have %d "
                    "scheduled visit(s). Please complete or cancel them first."
                ) % (doctor.full_name, scheduled_visits_count))
        return super(Doctor, self).action_archive()

    @api.depends('license_date')
    def _compute_experience(self):
        today = date.today()
        for doctor in self:
            if doctor.license_date:
                diff = relativedelta(today, doctor.license_date)
                doctor.experience = diff.years
            else:
                doctor.experience = 0

    # instead of name_get
    @api.depends('last_name', 'first_name', 'specialty_id')
    def _compute_display_name(self):
        for doctor in self:
            name = doctor.full_name or ""
            if doctor.specialty_id:
                doctor.display_name = f"{name} ({doctor.specialty_id.name})"
            else:
                doctor.display_name = name
