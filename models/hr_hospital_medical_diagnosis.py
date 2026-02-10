from odoo import models, fields

class MedicalDiagnosis(models.Model):
    """Model to store medical diagnoses made during patient visits."""
    _name = 'hr.hospital.medical.diagnosis'
    _description = 'Medical Diagnosis'

    # Relation to the visit (required for cascading deletion)
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        ondelete='cascade',
        required=True
    )

    # Relation to the disease
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True
    )

    # Detailed descriptions
    description = fields.Text(string='Diagnosis Description')
    treatment = fields.Html(string='Prescribed Treatment')

    # Approval information
    is_approved = fields.Boolean(
        string='Approved',
        default=False
    )
    approved_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Approved By',
        readonly=True
    )
    approval_date = fields.Datetime(
        string='Approval Date',
        readonly=True
    )

    # Clinical details
    severity = fields.Selection(
        selection=[
            ('light', 'Light'),
            ('medium', 'Medium'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
        string='Severity Degree'
    )