from odoo import models, fields

class PatientDoctorHistory(models.Model):
    """Model to track history of personal doctor assignments for patients."""
    _name = 'hr.hospital.patient.doctor.history'
    _description = 'Patient Doctor History'
    _order = 'appointment_date desc'

    # Relations
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        ondelete='restrict'
    )

    # Date and Reason
    appointment_date = fields.Date(
        required=True,
        default=fields.Date.context_today
    )
    change_date = fields.Date(
        help='Date when the doctor was replaced'
    )
    reason = fields.Text(string='Reason for Change')

    # Status
    active = fields.Boolean(
        default=True,
        help='If true, this is the current personal doctor'
    )