from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Visit(models.Model):
    """Model to manage patient visits to doctors."""
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    # Status and Type
    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No-show'),
        ],
        default='scheduled',
        required=True
    )
    visit_type = fields.Selection(
        selection=[
            ('primary', 'Primary'),
            ('follow_up', 'Follow-up'),
            ('preventive', 'Preventive'),
            ('urgent', 'Urgent'),
        ],
        default='primary'
    )

    # Timing
    planned_date = fields.Datetime(
        string='Planned Date and Time',
        required=True
    )
    actual_date = fields.Datetime(
        string='Actual Date and Time',
        help='Actual time when the visit took place'
    )

    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.specialty',
        string='Required Specialty'
    )
    filter_education_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Filter by Education Country'
    )

    # Relations
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain="[('license_number', '!=', False)]",
        help='Only doctors with a valid license number can be assigned to a visit.',
        required=True
    )

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        help='Mentor of the intern doctor',
        readonly=True
    )

    patient_lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Patient Language'
    )
    patient_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Patient Citizenship'
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        required=True
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.medical.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    diagnosis_count = fields.Integer(
        compute='_compute_diagnosis_count',
        readonly=True,
    )

    # Medical Notes
    recommendations = fields.Html()

    # Financial details
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id
    )
    visit_cost = fields.Monetary(
        currency_field='currency_id'
    )

    @api.constrains('planned_date', 'actual_date', 'doctor_id', 'patient_id')
    def _check_planned_date(self):
        for visit in self:
            if (not visit.planned_date or not visit.actual_date
                    or not visit.doctor_id or not visit.patient_id):
                continue

            if visit.actual_date < visit.planned_date:
                raise ValidationError(
                    self.env._("Actual date cannot be earlier than planned date!")
                )

            start_date = visit.planned_date.date() if visit.planned_date else None
            domain = [
                ('id', '!=', visit.id),
                ('doctor_id', '=', visit.doctor_id.id),
                ('patient_id', '=', visit.patient_id.id),
                ('planned_date', '>=', start_date),
                ('planned_date', '<', start_date + timedelta(days=1))
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    self.env._("This patient already has a scheduled"
                               " visit to this doctor on this day!")
                )

    def unlink(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise UserError(self.env._(
                    "You cannot delete the visit of patient %(name)s because it "
                    "already contains diagnoses. Please delete diagnoses first "
                    "or archive the visit instead.",
                    name=visit.patient_id.full_name
                ))
        return super().unlink()

    def write(self, vals):
        if any(field in vals for field in ['doctor_id', 'actual_date', 'planned_date']):
            for visit in self:
                if visit.state == 'completed':
                    if ('doctor_id' in vals
                            and vals['doctor_id'] != visit.doctor_id.id):
                        raise UserError(
                            self.env._('You cannot change Doctor for completed visit!')
                        )

                    if ('actual_date' in vals
                        and fields.Datetime.to_datetime(vals['actual_date']) != visit.actual_date):

                        raise UserError(
                            self.env._("You can't change Actual date"
                                       " or time for completed visit!")
                        )

                    if ('planned_date' in vals
                        and fields.Datetime.to_datetime(vals['planned_date'])
                            != visit.planned_date):
                        raise UserError(
                            self.env._("You can't change Planned date"
                                       " or time for completed visit!")
                        )

        return super().write(vals)

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        for visit in self:
            visit.diagnosis_count = len(visit.diagnosis_ids)

    @api.depends('planned_date', 'patient_id')
    def _compute_display_name(self):
        for visit in self:
            date_str = visit.planned_date.strftime('%Y-%m-%d %H:%M') \
                if visit.planned_date else self.env._("No Date")
            patient_name = visit.patient_id.display_name or self.env._("Unknown Patient")

            visit.display_name = f"{date_str} - {patient_name}"

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': self.env._("Patient Allergy Warning!"),
                    'message': self.env._(
                        "Note: Patient %(name)s has the"
                               " following allergies: \n\n %(allergies)s",
                               name=self.patient_id.full_name,
                               allergies=self.patient_id.allergies
                    ),
                    'type': 'notification',
                }
            }
        return {}

    @api.onchange('doctor_id')
    def _onchange_doctor_id_set_mentor(self):
        if self.doctor_id and self.doctor_id.is_intern:
            self.mentor_id = self.doctor_id.mentor_id
        else:
            self.mentor_id = False

    @api.onchange('specialty_id', 'planned_date', 'filter_education_country_id')
    def _onchange_filter_doctors(self):
        # Base domain
        doctor_domain = [
            ('specialty_id', '=', self.specialty_id.id),
            ('license_number', '!=', False)
        ]
        if self.filter_education_country_id:
            doctor_domain.append(
                ('education_country_id', '=', self.filter_education_country_id.id)
            )

        if self.planned_date:
            schedules = self.env['hr.hospital.doctor.schedule'].search([
                ('work_date', '=', self.planned_date.date()),
                ('schedule_type', '=', 'work')  # Only working days, not vacations
            ])

            # Extract doctor IDs
            available_doctor_ids = schedules.mapped('doctor_id').ids
            doctor_domain.append(('id', 'in', available_doctor_ids))

        return {'domain': {'doctor_id': doctor_domain}}

    @api.onchange('planned_date', 'doctor_id')
    def _onchange_planned_date_check_availability(self):
        if not self.planned_date or not self.doctor_id:
            return {}

        # Search for a 'working' schedule entry for this doctor and date
        schedule = self.env['hr.hospital.doctor.schedule'].search([
            ('doctor_id', '=', self.doctor_id.id),
            ('work_date', '=', self.planned_date.date() if self.planned_date else None),
            ('schedule_type', '=', 'work')
        ], limit=1)

        if not schedule:
            # Clear the date and show a warning
            selected_date = self.planned_date
            self.planned_date = False

            return {
                'warning': {
                    'title': self.env._("Doctor Unavailable"),
                    'message': self.env._(
                        "Doctor %(name)s does not have a working schedule for %(date)s. "
                        "Please select another date or check doctor's vacation/sick leaves.",
                        name=self.doctor_id.display_name, date=selected_date)
                }
            }
        return {}

    @api.onchange('patient_lang_id', 'patient_country_id')
    def _onchange_filter_patients(self):

        patient_domain = []

        if self.patient_lang_id:
            # Filter by the language
            patient_domain.append(('lang_id', '=', self.patient_lang_id.id))

        if self.patient_country_id:
            # Filter by the citizenship country
            patient_domain.append(('country_id', '=', self.patient_country_id.id))

        # Return the calculated domain
        return {'domain': {'patient_id': patient_domain}}
