from odoo import models, fields, api


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    # Новий лікар для всіх вибраних пацієнтів
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
        domain=[('is_intern', '=', False)]
    )

    # Field Many2many for patients from list or added manually
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
        required=True
    )

    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.context_today,
        required=True
    )

    reason = fields.Text(
        string='Reason for Change',
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super(MassReassignDoctorWizard, self).default_get(fields_list)
        # Get active patients from context
        active_ids = self.env.context.get('active_ids')
        if active_ids and self.env.context.get('active_model') == 'hr.hospital.patient':
            res.update({'patient_ids': [(6, 0, active_ids)]})
        return res

    def action_reassign(self):
        self.ensure_one()
        for patient in self.patient_ids:
            # Put reason and change_date to context
            # and update doctor
            patient.with_context(
                reassign_reason=self.reason,
                reassign_date=self.change_date
            ).write({'personal_doctor_id': self.new_doctor_id.id})

        return {'type': 'ir.actions.act_window_close'}
