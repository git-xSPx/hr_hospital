from odoo import models, fields


class DoctorSpecialty(models.Model):
    """Model to manage doctor specialties."""
    _name = 'hr.hospital.doctor.specialty'
    _description = 'Doctor Specialty'

    # Identity details
    name = fields.Char(
        string='Specialty Name',
        required=True
    )
    code = fields.Char(
        string='Specialty Code',
        size=10,
        required=True
    )
    description = fields.Text()

    # Status
    active = fields.Boolean(
        default=True
    )

    # Relations
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='specialty_id',
        string='Doctors'
    )
