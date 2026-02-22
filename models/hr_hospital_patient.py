from odoo import models, fields, api


class Patient(models.Model):
    """Model to manage patient information, inheriting from abstract person."""
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _inherit = 'hr.hospital.person'

    # Personal Doctor link
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
    )

    # Identification
    passport_data = fields.Char(
        string='Passport Details',
        size=10
    )

    # Contact Person link
    contact_person_id = fields.Many2one(
        comodel_name='hr.hospital.contact.person',
    )

    # Medical Info
    blood_group = fields.Selection(
        selection=[
            ('o+', 'O(I) Rh+'),
            ('o-', 'O(I) Rh-'),
            ('a+', 'A(II) Rh+'),
            ('a-', 'A(II) Rh-'),
            ('b+', 'B(III) Rh+'),
            ('b-', 'B(III) Rh-'),
            ('ab+', 'AB(IV) Rh+'),
            ('ab-', 'AB(IV) Rh-'),
        ],
    )
    allergies = fields.Text()

    # Insurance Info
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('is_company', '=', True)]
    )
    insurance_policy_number = fields.Char()

    # History (One2many relation to the history model)
    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.patient.doctor.history',
        inverse_name='patient_id',
        string='Personal Doctor History'
    )

    def write(self, vals):
        result = super().write(vals)
        if 'personal_doctor_id' in vals:
            for patient in self:
                self.env['hr.hospital.patient.doctor.history'].create({
                    'patient_id': patient.id,
                    'doctor_id': vals['personal_doctor_id'],
                    'appointment_date': fields.Date.today(),
                    'change_date': self.env.context.get('reassign_date')
                                   or fields.Date.today(),
                    'reason': self.env.context.get('reassign_reason')
                              or self.env._('Manual change'),
                })
        return result

    @api.depends('last_name', 'first_name')
    def _compute_display_name(self):
        for patient in self:
            name = f"{patient.last_name or ''} {patient.first_name or ''}".strip()
            patient.display_name = name or self.env._("New Patient")

    def action_view_visits(self):
        self.ensure_one()
        return {
            'name': self.env._('Patient Visits'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_view_diagnoses(self):
        self.ensure_one()
        return {
            'name': self.env._('Patient Diagnoses'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.medical.diagnosis',
            'view_mode': 'list,form',
            'domain': [('visit_id.patient_id', '=', self.id)],
        }

    def action_schedule_visit(self):
        self.ensure_one()
        context = {
            'default_patient_id': self.id,
        }

        if self.personal_doctor_id:
            context['default_doctor_id'] = self.personal_doctor_id.id
            if self.personal_doctor_id.specialty_id:
                context['default_specialty_id'] = self.personal_doctor_id.specialty_id.id

        if self.lang_id:
            context['default_patient_lang_id'] = self.lang_id.id

        if self.country_id:
            context['default_patient_country_id'] = self.country_id.id

        return {
            'name': self.env._('Schedule Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'context': context,
        }
