from odoo import models, fields


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
        string='Status',
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
        string='Visit Type',
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

    # Relations
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.medical.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    # Medical Notes
    recommendations = fields.Html(string='Recommendations')

    # Financial details
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    visit_cost = fields.Monetary(
        string='Visit Cost',
        currency_field='currency_id'
    )