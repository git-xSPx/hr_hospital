from odoo import models, fields, api
from odoo.tools.translate import _

class Patient(models.Model):
    """Model to manage patient information, inheriting from abstract person."""
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _inherit = 'hr.hospital.person'

    # Personal Doctor link
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor'
    )

    # Identification
    passport_data = fields.Char(
        string='Passport Details',
        size=10
    )

    # Contact Person link
    contact_person_id = fields.Many2one(
        comodel_name='hr.hospital.contact.person',
        string='Contact Person'
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
        string='Blood Group'
    )
    allergies = fields.Text(string='Allergies')

    # Insurance Info
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance Company',
        domain=[('is_company', '=', True)]
    )
    insurance_policy_number = fields.Char(string='Insurance Policy Number')

    # History (One2many relation to the history model)
    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.patient.doctor.history',
        inverse_name='patient_id',
        string='Personal Doctor History'
    )

    def write(self, vals):
        result = super(Patient, self).write(vals)
        if 'personal_doctor_id' in vals:
            for patient in self:
                self.env['hr.hospital.patient.doctor.history'].create({
                    'patient_id': patient.id,
                    'doctor_id': vals['personal_doctor_id'],
                    'appointment_date': fields.Date.today(),
                    'change_date': self.env.context.get('reassign_date') or fields.Date.today(),
                    'reason': self.env.context.get('reassign_reason') or _('Manual change'),
                })
        return result

    @api.depends('last_name', 'first_name')
    def _compute_display_name(self):
        for patient in self:
            name = f"{patient.last_name or ''} {patient.first_name or ''}".strip()
            patient.display_name = name or _("New Patient")
