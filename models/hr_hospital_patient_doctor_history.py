from odoo import models, fields, api


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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('active', True):

                patient_id = vals.get('patient_id')
                if patient_id:
                    old_active_histories = self.search([
                        ('patient_id', '=', patient_id),
                        ('active', '=', True),
                    ])
                    if old_active_histories:
                        old_active_histories.write({'active': False})

        return super(PatientDoctorHistory, self).create(vals_list)
